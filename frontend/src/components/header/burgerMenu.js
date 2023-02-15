import React from 'react';

import { MenuIcon, CloseIcon } from '../svgIcons';

export const BurgerMenu = React.forwardRef((props, ref) => (
  <button
    className="blue-dark bg-white br1 f5 bn pointer"
    style={{ padding: '0.5rem 1.5rem' }}
    ref={ref}
    aria-label="Menu"
    {...props}
  >
    {props.open ? (
      <CloseIcon style={{ width: '20px', height: '20px' }} />
    ) : (
      <MenuIcon style={{ width: '20px', height: '20px' }} />
    )}
  </button>
));
