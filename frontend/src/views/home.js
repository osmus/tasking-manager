import { ErrorBoundary } from 'react-error-boundary';
import { FormattedMessage } from 'react-intl';

import { Jumbotron, SecondaryJumbotron } from '../components/homepage/jumbotron';
import { StatsSection } from '../components/homepage/stats';
import { MappingFlow } from '../components/homepage/mappingFlow';
import { WhoIsMapping } from '../components/homepage/whoIsMapping';
import { Testimonials } from '../components/homepage/testimonials';
import { Alert } from '../components/alert';
import homeMessages from '../components/homepage/messages';
import StatsTimestamp from '../components/statsTimestamp/';

export function Home() {
  return (
    <div className="pull-center">
      <Jumbotron />
      <MappingFlow />
      <WhoIsMapping />
      <Testimonials />
      <SecondaryJumbotron />
    </div>
  );
}
