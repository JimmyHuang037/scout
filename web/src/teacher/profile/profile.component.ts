import { Component, Input } from '@angular/core';
import { Teacher } from '../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-teacher-profile',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule
  ],
  template: `
    <mat-card class="profile-card">
      <mat-card-header>
        <mat-card-title>教师信息</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="profile-info" *ngIf="teacher">
          <p><strong>教师编号：</strong>{{ teacher.teacher_id }}</p>
          <p><strong>教师姓名：</strong>{{ teacher.teacher_name }}</p>
        </div>
        <div *ngIf="!teacher" class="no-data">
          暂无教师信息
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .profile-card {
      margin-bottom: 20px;
    }
    
    .profile-info p {
      margin: 10px 0;
      font-size: 16px;
    }
    
    .no-data {
      text-align: center;
      color: #666;
      font-style: italic;
      padding: 20px;
    }
  `]
})
export class TeacherProfileComponent {
  @Input() teacher: Teacher | null = null;
}