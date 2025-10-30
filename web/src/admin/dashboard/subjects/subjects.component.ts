import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { AdminService } from '../../../shared/admin.service';
import { Subject } from '../../../shared/models';

@Component({
  selector: 'app-admin-subjects',
  standalone: true,
  imports: [
    CommonModule,
    MatTableModule,
    MatCardModule,
    MatProgressSpinnerModule,
    MatIconModule,
    MatButtonModule,
    MatFormFieldModule,
    MatInputModule,
    FormsModule
  ],
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <h2>科目管理</h2>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="toolbar">
          <mat-form-field appearance="outline">
            <mat-label>搜索科目</mat-label>
            <input matInput placeholder="输入科目名称" [(ngModel)]="searchTerm" (input)="applyFilter()">
          </mat-form-field>
          <button mat-raised-button color="primary" (click)="openCreateDialog()">
            <mat-icon>add</mat-icon>
            添加科目
          </button>
        </div>

        <div class="table-container">
          <table mat-table [dataSource]="filteredSubjects" class="subjects-table">
            <!-- 科目ID列 -->
            <ng-container matColumnDef="subject_id">
              <th mat-header-cell *matHeaderCellDef>科目ID</th>
              <td mat-cell *matCellDef="let subject">{{ subject.subject_id }}</td>
            </ng-container>

            <!-- 科目名称列 -->
            <ng-container matColumnDef="subject_name">
              <th mat-header-cell *matHeaderCellDef>科目名称</th>
              <td mat-cell *matCellDef="let subject">{{ subject.subject_name }}</td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let subject">
                <button mat-icon-button color="primary" (click)="editSubject(subject)" aria-label="编辑">
                  <mat-icon>edit</mat-icon>
                </button>
                <button mat-icon-button color="warn" (click)="deleteSubject(subject.subject_id)" aria-label="删除">
                  <mat-icon>delete</mat-icon>
                </button>
              </td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>

          <div class="loading-shade" *ngIf="loading">
            <mat-spinner></mat-spinner>
          </div>

          <div class="no-data" *ngIf="!loading && filteredSubjects.length === 0">
            <p>没有找到科目数据</p>
          </div>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .toolbar {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 20px;
      flex-wrap: wrap;
      gap: 10px;
    }

    .toolbar mat-form-field {
      flex: 1;
      min-width: 200px;
      max-width: 400px;
    }

    .table-container {
      position: relative;
      min-height: 400px;
    }

    .subjects-table {
      width: 100%;
    }

    .loading-shade {
      position: absolute;
      top: 0;
      left: 0;
      bottom: 0;
      right: 0;
      background: rgba(0, 0, 0, 0.15);
      z-index: 1;
      display: flex;
      align-items: center;
      justify-content: center;
    }

    .no-data {
      text-align: center;
      padding: 40px;
      color: #666;
    }

    mat-card-title h2 {
      margin: 0;
    }
  `]
})
export class SubjectsComponent implements OnInit {
  subjects: Subject[] = [];
  filteredSubjects: Subject[] = [];
  loading = false;
  searchTerm = '';
  
  displayedColumns: string[] = ['subject_id', 'subject_name', 'actions'];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadSubjects();
  }

  loadSubjects(): void {
    this.loading = true;
    // TODO: 实现获取科目列表的API调用
    // this.adminService.getSubjects().subscribe({
    //   next: (subjects) => {
    //     this.subjects = subjects;
    //     this.filteredSubjects = [...subjects];
    //     this.loading = false;
    //   },
    //   error: (error) => {
    //     console.error('加载科目数据失败:', error);
    //     this.loading = false;
    //   }
    // });
    
    // 模拟数据用于演示
    setTimeout(() => {
      this.subjects = [
        { subject_id: 1, subject_name: '语文' },
        { subject_id: 2, subject_name: '数学' },
        { subject_id: 3, subject_name: '英语' },
        { subject_id: 4, subject_name: '物理' },
        { subject_id: 5, subject_name: '化学' }
      ];
      this.filteredSubjects = [...this.subjects];
      this.loading = false;
    }, 1000);
  }

  applyFilter(): void {
    if (!this.searchTerm) {
      this.filteredSubjects = [...this.subjects];
      return;
    }
    
    const term = this.searchTerm.toLowerCase();
    this.filteredSubjects = this.subjects.filter(subject => 
      subject.subject_name.toLowerCase().includes(term)
    );
  }

  openCreateDialog(): void {
    // TODO: 打开创建科目对话框
    console.log('打开创建科目对话框');
  }

  editSubject(subject: Subject): void {
    // TODO: 打开编辑科目对话框
    console.log('编辑科目:', subject);
  }

  deleteSubject(subjectId: number): void {
    // TODO: 删除科目
    console.log('删除科目:', subjectId);
  }
}