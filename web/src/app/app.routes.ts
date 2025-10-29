import { Routes } from '@angular/router';
import { DashboardComponent as StudentDashboardComponent } from '../student/dashboard.component';
import { TeacherDashboardComponent } from '../teacher/dashboard.component';

export const routes: Routes = [
  { path: '', redirectTo: '/student/dashboard', pathMatch: 'full' },
  { path: 'student/dashboard', component: StudentDashboardComponent },
  { path: 'teacher/dashboard', component: TeacherDashboardComponent },
  { path: '**', redirectTo: '/student/dashboard' }
];