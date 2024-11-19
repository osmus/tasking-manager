import React, { useEffect, useState } from 'react';
import { useSelector, useDispatch } from 'react-redux';
import * as iD from '@osm-sandbox/public-domain-id';
import '@osm-sandbox/public-domain-id/dist/iD.css';

import { PD_CLIENT_ID, PD_CLIENT_SECRET, BASE_URL } from '../config';

export default function PDEditor({ setDisable, comment, presets, imagery, apiUrl, gpxUrl }) {

  const dispatch = useDispatch();
  const session = useSelector((state) => state.auth.session);
  const iDContext = useSelector((state) => state.editor.context);
  const locale = useSelector((state) => state.preferences.locale);
  const [customImageryIsSet, setCustomImageryIsSet] = useState(false);
  const windowInit = typeof window !== undefined;
  
  const customSource =
    iDContext && iDContext.background() && iDContext.background().findSource('custom');

  useEffect(() => {
    if (!customImageryIsSet && imagery && customSource) {
      if (imagery.startsWith('http')) {
        iDContext.background().baseLayerSource(customSource.template(imagery));
        setCustomImageryIsSet(true);
        // this line is needed to update the value on the custom background dialog
        window.iD.prefs('background-custom-template', imagery);
      } else {
        const imagerySource = iDContext.background().findSource(imagery);
        if (imagerySource) {
          iDContext.background().baseLayerSource(imagerySource);
        }
      }
    }
  }, [customImageryIsSet, imagery, iDContext, customSource]);
  
  useEffect(() => {
    return () => {
      dispatch({ type: 'SET_VISIBILITY', isVisible: true });
    };
    // eslint-disable-next-line
  }, []);

  useEffect(() => {
    if (windowInit) {
      dispatch({ type: 'SET_VISIBILITY', isVisible: false });
      if (iDContext === null) {
        // we need to keep iD context on redux store because iD works better if
        // the context is not restarted while running in the same browser session
        dispatch({ type: 'SET_EDITOR', context: window.iD.coreContext() });
      }
    }
  }, [windowInit, iDContext, dispatch]);

  useEffect(() => {
    if (iDContext && comment) {
      iDContext.defaultChangesetComment(comment);
    }
  }, [comment, iDContext]);

  useEffect(() => {

    if (session && locale && iD && iDContext) {
      // if presets is not a populated list we need to set it as null
      try {
        if (presets.length) {
          window.iD.presetManager.addablePresetIDs(presets);
        } else {
          window.iD.presetManager.addablePresetIDs(null);
        }
      } catch (e) {
        window.iD.presetManager.addablePresetIDs(null);
      }
      // setup the context
      iDContext
        .embed(true)
        .assetPath('/static/pdeditor/')
        .locale(locale)
        .setsDocumentTitle(false)
        .containerNode(document.getElementById('id-container'));
      // init the ui or restart if it was loaded previously
      if (iDContext.ui() !== undefined) {
        iDContext.reset();
        iDContext.ui().restart();
      } else {
        iDContext.init();
      }
      if (gpxUrl) {
        iDContext.layers().layer('data').url(gpxUrl, '.gpx');
      }

      iDContext.connection().switch({
        url: apiUrl,
        client_id: PD_CLIENT_ID,
        client_secret: PD_CLIENT_SECRET,
        //redirect_uri: BASE_URL + '/static/id/land.html',
      });

      const thereAreChanges = (changes) =>
        changes.modified.length || changes.created.length || changes.deleted.length;

      iDContext.history().on('change', () => {
        if (thereAreChanges(iDContext.history().changes())) {
          setDisable(true);
        } else {
          setDisable(false);
        }
      });
    }
  }, [session, iDContext, setDisable, presets, locale, gpxUrl]);

  return <div className="w-100 vh-minus-77-ns" id="id-container"></div>;
}
