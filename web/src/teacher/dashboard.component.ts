import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-teacher-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule
  ],
  template: `
    <mat-toolbar color="primary">
      <span>教师仪表板</span>
    </mat-toolbar>
    
    <div class="dashboard-container">
      <mat-card>
        <mat-card-content>
          <p>欢迎, {{teacherId}}!</p>
          <p>教师功能正在开发中...</p>
        </mat-card-content>
      </mat-card>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
    }
  `]
})
export class TeacherDashboardComponent implements OnInit {
  teacherId: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.teacherId = params['teacherId'] || null;
    });
  }
}