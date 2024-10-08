import { PureComponent } from 'react';

export class CloseIcon extends PureComponent {
  render() {
    return (
      <svg width="8" height="8" viewBox="0 0 8 8" {...this.props}>
        <path
          fill="currentColor"
          d="M1.41 0l-1.41 1.41.72.72 1.78 1.81-1.78 1.78-.72.69 1.41 1.44.72-.72 1.81-1.81 1.78 1.81.69.72 1.44-1.44-.72-.69-1.81-1.78 1.81-1.81.72-.72-1.44-1.41-.69.72-1.78 1.78-1.81-1.78-.72-.72z"
        />
      </svg>
    );
  }
}
