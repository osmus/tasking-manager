import { useState } from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';
import { MapDatabaseMessage } from '../mapDatabase';
import { Alert } from '../alert';

import {
  OrganisationSelect,
  SandboxBoxSelect,
} from '../formInputs';

export default function Review({ metadata, updateMetadata, selectedOrgObj, updateSelectedOrgObj, token, projectId, cloneProjectData }) {
  const [error, setError] = useState(null);

  const projectDatabaseOptions = [
    { value: 'OSM', label: 'OSM' },
    { value: 'SANDBOX', label: 'SANDBOX' },
  ];

  const setProjectName = (event) => {
    event.preventDefault();
    updateMetadata({ ...metadata, projectName: event.target.value });
  };

  return (
    <>
      <h3 className="f3 ttu fw6 mt2 mb3 barlow-condensed blue-dark">
        <FormattedMessage {...messages.step4} />
      </h3>
      <p className="pt2">
        <FormattedMessage
          {...messages.reviewTaskNumberMessage}
          values={{ n: metadata.tasksNumber }}
        />
      </p>

      {cloneProjectData.name === null ? (
        <>
          <label htmlFor="name" className="f5 fw6 db mb2 pt3">
            <FormattedMessage {...messages.name} />
          </label>
          <input
            onChange={setProjectName}
            id="name"
            className="input-reset ba b--black-20 pa2 mb2 db w-100"
            type="text"
          />
        </>
      ) : null}

      {cloneProjectData.organisation === null ? (
        <>
          <label className="f5 fw6 db mb2 pt3">
            <FormattedMessage {...messages.organization} />
          </label>
          <OrganisationSelect
            orgId={metadata.organisation}
            onChange={(value) => {
              setError(null);
              updateSelectedOrgObj(value);
              var updatedMeta = { ...metadata, organisation: value.organisationId || '' };
              if (!value.databases.includes('OSM')) updatedMeta.database = 'SANDBOX';
              if (!value.databases.includes('SANDBOX')) updatedMeta.database = 'OSM';
              updateMetadata(updatedMeta);
            }}
            className="z-5 w-75"
          />
        </>
      ) : null}

      {selectedOrgObj.databases ? (
        <>
          <label className="f5 fw6 db mb2 pt3">
            <FormattedMessage {...messages.database} />
          </label>
          {projectDatabaseOptions.map((option) => (
            <label className="dib pr5" key={option.value}>
              <input
                disabled={selectedOrgObj.databases.length < 2}
                value={option.value}
                checked={option.value === (metadata.database === 'OSM' ? 'OSM' : 'SANDBOX')}
                onChange={() =>
                  updateMetadata({
                    ...metadata,
                    database: option.value,
                  })
                }
                type="radio"
                className={`radio-input input-reset pointer v-mid dib h2 w2 mr2 br-100 ba b--blue-light`}
              />
              <MapDatabaseMessage db={option.label} />
            </label>
          ))}
        </>
      ) : null}

      {metadata.database !== "OSM" ? (
        <SandboxBoxSelect
          boxId={metadata.database}
          onChange={(option) => {
            setError(null);
            var updatedMeta = { ...metadata, database: option.name || '' };
            updateMetadata(updatedMeta);
          }}
          className="z-5 w-75 pt3"
        />
      ) : null}

      {selectedOrgObj.databases && selectedOrgObj.databases.length === 1 ? (
        <p className="pt2">
          <FormattedMessage {...messages[`limitedOrgDatabases${selectedOrgObj.databases[0]}`]} />
        </p>
      ) : null}

      {error && (
        <Alert type="error">
          <FormattedMessage {...messages.creationFailed} values={{ error: error }} />
        </Alert>
      )}
    </>
  );
}
