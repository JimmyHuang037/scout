import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { CommonModule } from '@angular/common';
import { MatToolbarModule } from '@angular/material/toolbar';
import { MatCardModule } from '@angular/material/card';

@Component({
  selector: 'app-admin-dashboard',
  standalone: true,
  imports: [
    CommonModule,
    MatToolbarModule,
    MatCardModule
  ],
  template: `
    <mat-toolbar color="primary">
      <span>管理员仪表板</span>
    </mat-toolbar>
    
    <div class="dashboard-container">
      <mat-card>
        <mat-card-content>
          <p>欢迎, {{adminId}}!</p>
          <p>管理员功能正在开发中...</p>
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
export class AdminDashboardComponent implements OnInit {
  adminId: string | null = null;

  constructor(private route: ActivatedRoute) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.adminId = params['adminId'] || null;
    });
  }
}