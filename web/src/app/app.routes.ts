import { Routes } from '@angular/router';
import { DashboardComponent as StudentDashboardComponent } from '../student/dashboard.component';
import { TeacherDashboardComponent } from '../teacher/dashboard.component';
import { LoginComponent } from '../auth/login.component';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', component: LoginComponent },
  { path: 'student/dashboard', component: StudentDashboardComponent },
  { path: 'teacher/dashboard', component: TeacherDashboardComponent },
  { path: '**', redirectTo: '/login' }
];