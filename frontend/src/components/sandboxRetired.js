import { Alert } from './alert';

/* The OSM Sandbox platform was shut down in July 2026. Projects created against
   a sandbox database are no longer editable, but they remain readable for their
   contribution history. Everything in this file is transitional and should
   be dropped once these projects have been archived and the projects.database
   column is gone. */

export function isSandboxProject(project) {
  return Boolean(project && project.database);
}

export function SandboxRetiredNotice() {
  return (
    <Alert type="warning">
      This project used the OSM Sandbox, which has been retired. The project is kept here
      for its history, but its tasks can no longer be mapped or validated.
    </Alert>
  );
}
