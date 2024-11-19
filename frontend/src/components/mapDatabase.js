import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';

export const MapDatabaseMessage = (props) => {
  const { db, ...otherProps } = props;
  const id = ['OSM', ''].includes(db) ? 'OSM' : 'PDMAP';
  const message = <FormattedMessage {...messages[`database${id}`]} />;
  return <span {...otherProps}>{message}</span>;
};
