import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';

export const MapDatabaseMessage = (props) => {
  const { db, ...otherProps } = props;

  let message;
  if (db === 'ALL') {
    message = messages.databaseALL;
  } else if (db === 'OSM' || db === '') {
    message = messages.databaseOSM;
  } else {
    message = messages.databaseSANDBOX;
  }

  return <span {...otherProps}><FormattedMessage {...message}/></span>;
};
