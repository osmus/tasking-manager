import React, { useEffect, useState } from "react";
import { useSelector, useDispatch } from "react-redux";
import PropTypes from "prop-types";
import * as Rapid from "@osm-sandbox/sandbox-rapid";
import "@osm-sandbox/sandbox-rapid/dist/rapid.css";

import { getSandboxAuthToken } from "../store/actions/auth";
import { useSandboxOAuthCallback } from "../hooks/UseSandboxOAuthCallback";
import { getValidTokenOrInitiateAuth, fetchSandboxLicense } from "../utils/sandboxUtils";
import { types } from "../store/actions/editor";

const ASSET_PATH = "/static/sandbox-rapid/";

/**
 * Check if two URL search parameters are semantically equal
 * @param {URLSearchParams} first
 * @param {URLSearchParams} second
 * @return {boolean} true if they are semantically equal
 */
function equalsUrlParameters(first, second) {
  if (first.size === second.size) {
    for (const [key, value] of first) {
      if (!second.has(key) || second.get(key) !== value) {
        return false;
      }
    }
    return true;
  }
  return false;
}

/**
 * Update the URL (this also fires a hashchange event)
 * @param {URLSearchParams} hashParams the URL hash parameters
 */
function updateUrl(hashParams) {
  const oldUrl = window.location.href;
  // URLSearchParams.toString() encodes spaces as '+', not '%20' (it's application/x-www-form-urlencoded).
  // Rapid uses decodeURIComponent which does NOT convert '+' back to ' ' though. So to make roundtripping
  // work as expected, we'll replace '+' with '%20' in the encodeded output. This is safe because literal
  // plus characters will have been encoded to '%2B'.
  const hashString = hashParams.toString().replace(/\+/g, '%20');
  const newUrl = window.location.pathname + window.location.search + "#" + hashString;
  window.history.pushState(null, "", newUrl);
  window.dispatchEvent(
    new HashChangeEvent("hashchange", {
      newUrl: newUrl,
      oldUrl: oldUrl,
    }),
  );
}

/**
 * Generate the starting hash for the project
 * @param {string | undefined} comment The comment to use
 * @param {Array.<String> | undefined} presets The presets
 * @param {string | undefined} gpxUrl The task boundaries
 * @param {boolean | undefined} powerUser if the user should be shown advanced options
 * @param {string | undefined} imagery The imagery to use for the task
 * @param {string | undefined} license The license mode (cc0 for public domain)
 * @return {module:url.URLSearchParams | boolean} the new URL search params or {@code false} if no parameters changed
 */
function generateStartingHash({ comment, presets, gpxUrl, powerUser, imagery, license }) {
  const hashParams = new URLSearchParams(window.location.hash.substring(1));
  if (comment) {
    hashParams.set("comment", comment);
  }
  if (gpxUrl) {
    hashParams.set("data", gpxUrl);
  }
  if (powerUser !== undefined) {
    hashParams.set("poweruser", powerUser.toString());
  }
  if (presets) {
    hashParams.set("presets", presets.join(","));
  }
  if (imagery) {
    if (imagery.startsWith("http")) {
      hashParams.set("background", "custom:" + imagery);
    } else {
      hashParams.set("background", imagery);
    }
  }
  if (license) {
    hashParams.set("license", license);
  }
  if (equalsUrlParameters(hashParams, new URLSearchParams(window.location.hash.substring(1)))) {
    return false;
  }
  return hashParams;
}

/**
 * Resize rapid
 * @param {Context} rapidContext The rapid context to resize
 */
function resizeRapid(rapidContext) {
  // Get rid of black bars when toggling the TM sidebar
  const uiSystem = rapidContext?.systems?.ui;
  if (uiSystem?.started) {
    uiSystem.resize();
  }
}

/**
 * Update the disable state for the sidebar map actions
 * @param {function(boolean)} setDisable
 * @param {EditSystem} editSystem The edit system
 */
function updateDisableState(setDisable, editSystem) {
  if (editSystem.hasChanges()) {
    setDisable(true);
  } else {
    setDisable(false);
  }
}

export default function SandboxRapidEditor({
  setDisable,
  comment,
  presets,
  imagery,
  sandboxId,
  gpxUrl,
  powerUser = false,
  showSidebar = true,
}) {
  const dispatch = useDispatch();
  const session = useSelector((state) => state.auth.session);
  const sandboxTokens = useSelector((state) => state.auth.sandboxTokens);
  const sandboxAuthError = useSelector((state) => state.auth.sandboxAuthError);
  const { context, dom } = useSelector((state) => state.editor.rapidContext);
  const locale = useSelector((state) => state.preferences.locale);
  const [isInitialized, setIsInitialized] = useState(false);

  useSandboxOAuthCallback(sandboxId);

  useEffect(() => {
    if (context === null) {
      const dom = document.createElement("div");
      dom.className = "w-100 vh-minus-69-ns";

      const context = new Rapid.Context();
      context.embed(true);
      context.containerNode = dom;
      context.assetPath = ASSET_PATH;

      dispatch({ type: types.SET_RAPIDEDITOR, context: { context, dom } });
    }
  }, [context, dispatch]);

  useEffect(() => {
    if (context) {
      context.locale = locale;
    }
  }, [context, locale]);

  // Authenticate to Dashboard API and get an OAuth token for the sandbox
  useEffect(() => {
    const authenticate = async () => {
      if (!session || !locale || !context || isInitialized) {
        return;
      }

      const tokenData = await getValidTokenOrInitiateAuth({
        dispatch,
        sandboxId,
        sandboxTokens,
        getSandboxAuthToken,
      });

      if (!tokenData) {
        // auth flow was initiated (user will be redirected)
        return;
      }

      const license = await fetchSandboxLicense(sandboxId);
      context.license = license;

      // Generate hash parameters with license info
      const newParams = generateStartingHash({
        comment,
        presets,
        gpxUrl,
        powerUser,
        imagery,
        license,
      });
      if (newParams) {
        updateUrl(newParams);
      }

      setIsInitialized(true);
    };

    authenticate();
  }, [
    session,
    context,
    setDisable,
    presets,
    locale,
    gpxUrl,
    sandboxId,
    sandboxTokens,
    dispatch,
    isInitialized,
    comment,
    powerUser,
    imagery,
  ]);

  // Configure editor with sandbox API URL and OAuth token
  useEffect(() => {
    const tokenData = sandboxTokens[sandboxId];
    if (context && isInitialized && tokenData && tokenData.access_token) {
      context.preauth = {
        url: tokenData.sandbox_api_url.replace("/api/0.6", ""),
        apiUrl: tokenData.sandbox_api_url,
        access_token: tokenData.access_token,
      };
      context.apiConnections = [context.preauth];
    }
  }, [context, isInitialized, sandboxTokens, sandboxId]);

  // Set up event listeners to handle Rapid state changes
  useEffect(() => {
    const containerRoot = document.getElementById("sandbox-rapid-container-root");
    const editListener = () => updateDisableState(setDisable, context.systems.editor);

    if (context && dom && isInitialized) {
      containerRoot.appendChild(dom);

      let promise;
      if (context?.systems?.ui !== undefined) {
        resizeRapid(context);
        promise = Promise.resolve();
      } else {
        promise = context.initAsync();
      }

      promise.then(() => {
        if (context?.systems?.editor) {
          const editSystem = context.systems.editor;
          editSystem.on("stablechange", editListener);
          editSystem.on("reset", editListener);
        }
      });
    }

    return () => {
      if (containerRoot?.childNodes && dom in containerRoot.childNodes) {
        containerRoot?.removeChild(dom);
      }
      if (context?.systems?.editor) {
        const editSystem = context.systems.editor;
        editSystem.off("stablechange", editListener);
        editSystem.off("reset", editListener);
      }
    };
  }, [dom, context, setDisable, isInitialized]);

  // Resize the editor when sidebar shows/hides
  useEffect(() => {
    resizeRapid(context);
    return () => resizeRapid(context);
  }, [showSidebar, context]);

  useEffect(() => {
    if (context?.systems?.editor) {
      return () => context.systems.editor.saveBackup();
    }
  }, [context]);

  // Show error message if authentication failed
  if (sandboxAuthError) {
    return (
      <div className="w-100 vh-minus-69-ns flex items-center justify-center">
        <div className="bg-washed-red pa4 br2 ma3">
          <h3 className="red mt0">Sandbox Connection Error</h3>
          <p className="mt2 mb3">{sandboxAuthError}</p>
          <button
            className="bg-red white pa2 br2 bn pointer dim"
            onClick={() => {
              dispatch({ type: "CLEAR_SANDBOX_AUTH_ERROR" });
              window.location.reload();
            }}
          >
            Retry
          </button>
        </div>
      </div>
    );
  }

  return <div className="w-100 vh-minus-69-ns" id="sandbox-rapid-container-root"></div>;
}

SandboxRapidEditor.propTypes = {
  setDisable: PropTypes.func,
  comment: PropTypes.string,
  presets: PropTypes.array,
  imagery: PropTypes.string,
  sandboxId: PropTypes.string.isRequired,
  gpxUrl: PropTypes.string.isRequired,
  powerUser: PropTypes.bool,
  showSidebar: PropTypes.bool,
};
