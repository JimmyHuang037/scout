import { Routes } from '@angular/router';
import { LoginComponent } from '../auth/login.component';
import { DashboardComponent as StudentDashboardComponent } from '../student/dashboard.component';
import { DashboardComponent as TeacherDashboardComponent } from '../teacher/dashboard.component';

export const routes: Routes = [
  {
    path: '',
    redirectTo: '/login',
    pathMatch: 'full'
  },
  {
    path: 'login',
    component: LoginComponent//可搜索
  },
  {
    path: 'student/dashboard',
    component: StudentDashboardComponent
  },
  {
    path: 'teacher/dashboard',
    component: TeacherDashboardComponent
  },
  {
    path: 'admin/dashboard',
    loadComponent: () => import('../admin/dashboard.component').then(m => m.AdminDashboardComponent)
  }
];