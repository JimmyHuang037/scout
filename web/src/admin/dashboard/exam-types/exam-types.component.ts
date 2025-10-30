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
import { ExamType } from '../../../shared/models';

@Component({
  selector: 'app-admin-exam-types',
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
          <h2>考试类型管理</h2>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="toolbar">
          <mat-form-field appearance="outline">
            <mat-label>搜索考试类型</mat-label>
            <input matInput placeholder="输入考试类型名称" [(ngModel)]="searchTerm" (input)="applyFilter()">
          </mat-form-field>
          <button mat-raised-button color="primary" (click)="openCreateDialog()">
            <mat-icon>add</mat-icon>
            添加考试类型
          </button>
        </div>

        <div class="table-container">
          <table mat-table [dataSource]="filteredExamTypes" class="exam-types-table">
            <!-- 考试类型ID列 -->
            <ng-container matColumnDef="exam_type_id">
              <th mat-header-cell *matHeaderCellDef>考试类型ID</th>
              <td mat-cell *matCellDef="let examType">{{ examType.exam_type_id }}</td>
            </ng-container>

            <!-- 考试类型名称列 -->
            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef>考试类型名称</th>
              <td mat-cell *matCellDef="let examType">{{ examType.exam_name }}</td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let examType">
                <button mat-icon-button color="primary" (click)="editExamType(examType)" aria-label="编辑">
                  <mat-icon>edit</mat-icon>
                </button>
                <button mat-icon-button color="warn" (click)="deleteExamType(examType.exam_type_id)" aria-label="删除">
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

          <div class="no-data" *ngIf="!loading && filteredExamTypes.length === 0">
            <p>没有找到考试类型数据</p>
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

    .exam-types-table {
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
export class ExamTypesComponent implements OnInit {
  examTypes: ExamType[] = [];
  filteredExamTypes: ExamType[] = [];
  loading = false;
  searchTerm = '';
  
  displayedColumns: string[] = ['exam_type_id', 'exam_name', 'actions'];

  constructor(private adminService: AdminService) {}

  ngOnInit(): void {
    this.loadExamTypes();
  }

  loadExamTypes(): void {
    this.loading = true;
    this.adminService.getExamTypes().subscribe({
      next: (examTypes) => {
        this.examTypes = examTypes;
        this.filteredExamTypes = [...examTypes];
        this.loading = false;
      },
      error: (error) => {
        console.error('加载考试类型数据失败:', error);
        this.loading = false;
      }
    });
  }

  applyFilter(): void {
    if (!this.searchTerm) {
      this.filteredExamTypes = [...this.examTypes];
      return;
    }
    
    const term = this.searchTerm.toLowerCase();
    this.filteredExamTypes = this.examTypes.filter(examType => 
      examType.exam_name.toLowerCase().includes(term)
    );
  }

  openCreateDialog(): void {
    // TODO: 打开创建考试类型对话框
    console.log('打开创建考试类型对话框');
  }

  editExamType(examType: ExamType): void {
    // TODO: 打开编辑考试类型对话框
    console.log('编辑考试类型:', examType);
  }

  deleteExamType(examTypeId: number): void {
    // TODO: 删除考试类型
    console.log('删除考试类型:', examTypeId);
  }
}