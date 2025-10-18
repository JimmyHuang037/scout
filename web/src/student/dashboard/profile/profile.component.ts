import { Component, Input } from '@angular/core';
import { Student } from '../../../shared/models';
import { NgIf } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [
    NgIf,
    MatCardModule,
    MatListModule
  ],
  template: `
    <mat-card class="section">
      <mat-card-header>
        <mat-card-title>个人信息</mat-card-title>
      </mat-card-header>
      <mat-card-content *ngIf="student">
        <mat-list>
          <mat-list-item>
            <span class="label">姓名:</span>
            <span>{{student.student_name}}</span>
          </mat-list-item>
          <mat-list-item>
            <span class="label">学号:</span>
            <span>{{student.student_id}}</span>
          </mat-list-item>
          <mat-list-item>
            <span class="label">班级:</span>
            <span>{{student.class_name}}</span>
          </mat-list-item>
        </mat-list>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .section {
      margin-bottom: 30px;
    }

    .label {
      font-weight: bold;
      color: #555;
      display: inline-block;
      width: 60px;
      margin-right: 10px;
    }

    mat-list-item {
      height: auto !important;
      padding: 5px 0;
    }
  `]
})
export class ProfileComponent {
  @Input() student: Student | null = null;
}