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
import { Class } from '../../../shared/models';

@Component({
  selector: 'app-admin-classes',
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
          <h2>班级管理</h2>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="toolbar">
          <mat-form-field appearance="outline">
            <mat-label>搜索班级</mat-label>
            <input matInput placeholder="输入班级名称" [(ngModel)]="searchTerm" (input)="applyFilter()">
          </mat-form-field>
          <button mat-raised-button color="primary" (click)="openCreateDialog()">
            <mat-icon>add</mat-icon>
            添加班级
          </button>
        </div>

        <div class="table-container">
          <table mat-table [dataSource]="filteredClasses" class="classes-table">
            <!-- 班级ID列 -->
            <ng-container matColumnDef="class_id">
              <th mat-header-cell *matHeaderCellDef>班级ID</th>
              <td mat-cell *matCellDef="let cls">{{ cls.class_id }}</td>
            </ng-container>

            <!-- 班级名称列 -->
            <ng-container matColumnDef="class_name">
              <th mat-header-cell *matHeaderCellDef>班级名称</th>
              <td mat-cell *matCellDef="let cls">{{ cls.class_name }}</td>
            </ng-container>

            <!-- 班主任列 -->
            <ng-container matColumnDef="teacher_name">
              <th mat-header-cell *matHeaderCellDef>班主任</th>
              <td mat-cell *matCellDef="let cls">{{ cls.teacher_name }}</td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let cls">
                <button mat-icon-button color="primary" (click)="editClass(cls)" aria-label="编辑">
                  <mat-icon>edit</mat-icon>
                </button>
                <button mat-icon-button color="warn" (click)="deleteClass(cls.class_id)" aria-label="删除">
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

          <div class="no-data" *ngIf="!loading && filteredClasses.length === 0">
            <p>没有找到班级数据</p>
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

    .classes-table {
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
export class ClassesComponent implements OnInit {
  classes: Class[] = [];
  filteredClasses: Class[] = [];
  loading = false;
  searchTerm = '';
  
  displayedColumns: string[] = ['class_id', 'class_name', 'teacher_name', 'actions'];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadClasses();
  }

  loadClasses(): void {
    this.loading = true;
    // TODO: 实现获取班级列表的API调用
    // this.adminService.getClasses().subscribe({
    //   next: (classes) => {
    //     this.classes = classes;
    //     this.filteredClasses = [...classes];
    //     this.loading = false;
    //   },
    //   error: (error) => {
    //     console.error('加载班级数据失败:', error);
    //     this.loading = false;
    //   }
    // });
    
    // 模拟数据用于演示
    setTimeout(() => {
      this.classes = [
        { class_id: 1, class_name: '一年级一班', teacher_name: '张老师' },
        { class_id: 2, class_name: '一年级二班', teacher_name: '李老师' },
        { class_id: 3, class_name: '二年级一班', teacher_name: '王老师' }
      ];
      this.filteredClasses = [...this.classes];
      this.loading = false;
    }, 1000);
  }

  applyFilter(): void {
    if (!this.searchTerm) {
      this.filteredClasses = [...this.classes];
      return;
    }
    
    const term = this.searchTerm.toLowerCase();
    this.filteredClasses = this.classes.filter(cls => 
      cls.class_name.toLowerCase().includes(term) ||
      cls.teacher_name.toLowerCase().includes(term)
    );
  }

  openCreateDialog(): void {
    // TODO: 打开创建班级对话框
    console.log('打开创建班级对话框');
  }

  editClass(cls: Class): void {
    // TODO: 打开编辑班级对话框
    console.log('编辑班级:', cls);
  }

  deleteClass(classId: number): void {
    // TODO: 删除班级
    console.log('删除班级:', classId);
  }
}