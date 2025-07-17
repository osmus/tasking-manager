import React from 'react';
import { FormattedMessage } from 'react-intl';

import messages from './messages';

export const MapDatabaseMessage = (props) => {
  const { db, ...otherProps } = props;
  const message = <FormattedMessage {...messages[`database${db}`]} />;
  return <span {...otherProps}>{message}</span>;
};
