import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { AdminService } from '../shared/admin.service';

// 导入管理组件
import { StudentsComponent } from './dashboard/students/students.component';
import { TeachersComponent } from './dashboard/teachers/teachers.component';
import { ClassesComponent } from './dashboard/classes/classes.component';
import { SubjectsComponent } from './dashboard/subjects/subjects.component';
import { ExamTypesComponent } from './dashboard/exam-types/exam-types.component';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule,
    MatTabsModule,
    RouterModule,
    StudentsComponent,
    TeachersComponent,
    ClassesComponent,
    SubjectsComponent,
    ExamTypesComponent
  ],
  template: `
    <mat-toolbar color="primary">
      <span>管理员仪表板</span>
    </mat-toolbar>
    
    <div class="dashboard-container" *ngIf="adminId !== null">
      <h1>管理员功能</h1>
      
      <mat-tab-group dynamicHeight>
        <mat-tab label="学生管理">
          <app-admin-students></app-admin-students>
        </mat-tab>
        
        <mat-tab label="教师管理">
          <app-admin-teachers></app-admin-teachers>
        </mat-tab>
        
        <mat-tab label="班级管理">
          <app-admin-classes></app-admin-classes>
        </mat-tab>
        
        <mat-tab label="科目管理">
          <app-admin-subjects></app-admin-subjects>
        </mat-tab>
        
        <mat-tab label="考试类型管理">
          <app-admin-exam-types></app-admin-exam-types>
        </mat-tab>
      </mat-tab-group>
    </div>
    
    <div *ngIf="adminId === null" class="error-message">
      未提供管理员ID参数
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
      max-width: 1200px;
      margin: 0 auto;
    }
    
    .error-message {
      padding: 20px;
      text-align: center;
      color: #f44336;
    }
    
    h1 {
      color: #333;
      margin-bottom: 20px;
    }
    
    .tab-content {
      padding: 20px;
    }
  `]
})
export class AdminDashboardComponent implements OnInit {
  adminId: string | null = null;

  constructor(
    private route: ActivatedRoute,
    private adminService: AdminService
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.adminId = params['adminId'] || null;
    });
  }
}