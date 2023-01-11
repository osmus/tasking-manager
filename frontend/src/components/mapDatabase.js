import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';

export const MapDatabaseMessage = (props) => {
  const { db, ...otherProps } = props;
  const message = ['ALL', 'PDMAP', 'OSM'].includes(db) ? (
    <FormattedMessage {...messages[`database${db}`]} />
  ) : (
    db
  );
  return <span {...otherProps}>{message}</span>;
};
