import React from 'react';
import { Link } from '@gatsbyjs/reach-router';

export const NavLink = ({ partial = true, ...props }) => (
  <Link
    {...props}
    getProps={({ isCurrent, isPartiallyCurrent }) => {
      const isActive = partial ? isPartiallyCurrent : isCurrent;
      return { className: `${isActive && 'bg-blue-dark white'} ${props.className}` };
    }}
  />
);

export const TopNavLink = (props) => {
  const { isActive, ...otherProps } = props;
  return (
    <Link getProps={isActive} {...otherProps}>
      {props.children}
    </Link>
  );
};
