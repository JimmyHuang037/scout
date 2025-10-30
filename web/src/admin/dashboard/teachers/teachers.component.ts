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
import { Teacher } from '../../../shared/models';

@Component({
  selector: 'app-admin-teachers',
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
          <h2>教师管理</h2>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="toolbar">
          <mat-form-field appearance="outline">
            <mat-label>搜索教师</mat-label>
            <input matInput placeholder="输入教师姓名" [(ngModel)]="searchTerm" (input)="applyFilter()">
          </mat-form-field>
          <button mat-raised-button color="primary" (click)="openCreateDialog()">
            <mat-icon>add</mat-icon>
            添加教师
          </button>
        </div>

        <div class="table-container">
          <table mat-table [dataSource]="filteredTeachers" class="teachers-table">
            <!-- 教师ID列 -->
            <ng-container matColumnDef="teacher_id">
              <th mat-header-cell *matHeaderCellDef>教师ID</th>
              <td mat-cell *matCellDef="let teacher">{{ teacher.teacher_id }}</td>
            </ng-container>

            <!-- 姓名列 -->
            <ng-container matColumnDef="teacher_name">
              <th mat-header-cell *matHeaderCellDef>姓名</th>
              <td mat-cell *matCellDef="let teacher">{{ teacher.teacher_name }}</td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let teacher">
                <button mat-icon-button color="primary" (click)="editTeacher(teacher)" aria-label="编辑">
                  <mat-icon>edit</mat-icon>
                </button>
                <button mat-icon-button color="warn" (click)="deleteTeacher(teacher.teacher_id)" aria-label="删除">
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

          <div class="no-data" *ngIf="!loading && filteredTeachers.length === 0">
            <p>没有找到教师数据</p>
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

    .teachers-table {
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
export class TeachersComponent implements OnInit {
  teachers: Teacher[] = [];
  filteredTeachers: Teacher[] = [];
  loading = false;
  searchTerm = '';
  
  displayedColumns: string[] = ['teacher_id', 'teacher_name', 'actions'];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadTeachers();
  }

  loadTeachers(): void {
    this.loading = true;
    // TODO: 实现获取教师列表的API调用
    // this.adminService.getTeachers().subscribe({
    //   next: (teachers) => {
    //     this.teachers = teachers;
    //     this.filteredTeachers = [...teachers];
    //     this.loading = false;
    //   },
    //   error: (error) => {
    //     console.error('加载教师数据失败:', error);
    //     this.loading = false;
    //   }
    // });
    
    // 模拟数据用于演示
    setTimeout(() => {
      this.teachers = [
        { teacher_id: 1, teacher_name: '张老师' },
        { teacher_id: 2, teacher_name: '李老师' },
        { teacher_id: 3, teacher_name: '王老师' }
      ];
      this.filteredTeachers = [...this.teachers];
      this.loading = false;
    }, 1000);
  }

  applyFilter(): void {
    if (!this.searchTerm) {
      this.filteredTeachers = [...this.teachers];
      return;
    }
    
    const term = this.searchTerm.toLowerCase();
    this.filteredTeachers = this.teachers.filter(teacher => 
      teacher.teacher_name.toLowerCase().includes(term)
    );
  }

  openCreateDialog(): void {
    // TODO: 打开创建教师对话框
    console.log('打开创建教师对话框');
  }

  editTeacher(teacher: Teacher): void {
    // TODO: 打开编辑教师对话框
    console.log('编辑教师:', teacher);
  }

  deleteTeacher(teacherId: number): void {
    // TODO: 删除教师
    console.log('删除教师:', teacherId);
  }
}