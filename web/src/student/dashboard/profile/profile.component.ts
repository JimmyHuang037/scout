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
        <mat-card-title>学生信息</mat-card-title>
      </mat-card-header>
      @if (student) {
        <mat-card-content>
          <p><strong>姓名:</strong> {{student.student_name}}</p>
          <p><strong>班级:</strong> {{student.class_name}}</p>
        </mat-card-content>
      }
    </mat-card>
  `,
  styles: [`
    .section {
      margin-bottom: 30px;
    }

    .label {
      font-weight: bold;
      margin-right: 10px;
    }
  `]
})
export class ProfileComponent {
  @Input() student: Student | null = null;
}