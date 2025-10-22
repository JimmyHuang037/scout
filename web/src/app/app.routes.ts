import { Routes } from '@angular/router';
import { LoginComponent } from '../auth/login.component';
import { DashboardComponent } from '../student/dashboard/dashboard.component';

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
    component: DashboardComponent
  },
  {
    path: 'teacher/dashboard',
    loadComponent: () => import('../teacher/dashboard.component').then(m => m.TeacherDashboardComponent)
  },
  {
    path: 'admin/dashboard',
    loadComponent: () => import('../admin/dashboard.component').then(m => m.AdminDashboardComponent)
  }
];