import { bootstrapApplication } from '@angular/platform-browser';
import { studentAppConfig } from './src/student/app.config';
import { StudentAppComponent } from './src/student/app';

bootstrapApplication(StudentAppComponent, studentAppConfig)
  .catch((err) => console.error(err));