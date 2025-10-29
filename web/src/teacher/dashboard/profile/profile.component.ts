import { Component, Input } from '@angular/core';
import { Teacher } from '../../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { MatListModule } from '@angular/material/list';

@Component({
  selector: 'app-profile',
  standalone: true,
  imports: [MatCardModule, MatListModule],
  template: `
    <mat-card class="profile-card">
      <mat-card-header>
        <mat-card-title>教师信息</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        @if (teacher) {
          <mat-list>
            <mat-list-item>
              <span class="info-label">教师ID:</span>
              <span class="info-value">{{teacher.teacher_id}}</span>
            </mat-list-item>
            <mat-list-item>
              <span class="info-label">教师姓名:</span>
              <span class="info-value">{{teacher.teacher_name}}</span>
            </mat-list-item>
          </mat-list>
        } @else {
          <p>加载中...</p>
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .profile-card {
      margin-bottom: 16px;
    }
    .info-label {
      font-weight: bold;
      margin-right: 8px;
      min-width: 80px;
      display: inline-block;
    }
    .info-value {
      flex: 1;
    }
    mat-list-item {
      height: auto !important;
      margin: 8px 0;
    }
  `]
})
export class ProfileComponent {
  @Input() teacher: Teacher | null = null;
}