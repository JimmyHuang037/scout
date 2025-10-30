import { Component, OnInit, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { AdminService } from '../../../shared/admin.service';
import { Student } from '../../../shared/models';
import { CreateStudentDialogComponent } from './create-student-dialog.component';

@Component({
  selector: 'app-admin-students',
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
    FormsModule,
    MatPaginatorModule,
    MatSortModule,
    MatDialogModule,
    CreateStudentDialogComponent
  ],
  template: `
    <mat-card>
      <mat-card-header>
        <mat-card-title>
          <h2>学生管理</h2>
        </mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="toolbar">
          <mat-form-field appearance="outline">
            <mat-label>搜索学生</mat-label>
            <input matInput placeholder="输入学生ID或姓名" [(ngModel)]="searchTerm" (input)="applyFilter()">
          </mat-form-field>
          <button mat-raised-button color="primary" (click)="openCreateDialog()">
            <mat-icon>add</mat-icon>
            添加学生
          </button>
        </div>

        <div class="table-container">
          <table mat-table [dataSource]="dataSource" matSort class="students-table">
            <!-- 学生ID列 -->
            <ng-container matColumnDef="student_id">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>学生ID</th>
              <td mat-cell *matCellDef="let student">{{ student.student_id }}</td>
            </ng-container>

            <!-- 学生姓名列 -->
            <ng-container matColumnDef="student_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>学生姓名</th>
              <td mat-cell *matCellDef="let student">{{ student.student_name }}</td>
            </ng-container>

            <!-- 班级列 -->
            <ng-container matColumnDef="class_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>班级</th>
              <td mat-cell *matCellDef="let student">{{ student.class_name }}</td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let student">
                <button mat-icon-button color="primary" (click)="editStudent(student)" aria-label="编辑">
                  <mat-icon>edit</mat-icon>
                </button>
                <button mat-icon-button color="warn" (click)="deleteStudent(student.student_id)" aria-label="删除">
                  <mat-icon>delete</mat-icon>
                </button>
              </td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>

          <mat-paginator [pageSizeOptions]="[5, 10, 20]" showFirstLastButtons aria-label="选择页面">
          </mat-paginator>

          <div class="loading-shade" *ngIf="loading">
            <mat-spinner></mat-spinner>
          </div>

          <div class="no-data" *ngIf="!loading && dataSource.data.length === 0">
            <p>没有找到学生数据</p>
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

    .students-table {
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
export class StudentsComponent implements OnInit, AfterViewInit {
  students: Student[] = [];
  dataSource = new MatTableDataSource<Student>();
  loading = false;
  searchTerm = '';
  
  displayedColumns: string[] = ['student_id', 'student_name', 'class_name', 'actions'];

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  constructor(
    private adminService: AdminService,
    private dialog: MatDialog
  ) {}

  ngOnInit(): void {
    this.loadStudents();
  }

  ngAfterViewInit(): void {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  loadStudents(): void {
    this.loading = true;
    this.adminService.getStudents().subscribe({
      next: (students) => {
        this.students = students;
        this.dataSource.data = students;
        this.loading = false;
      },
      error: (error) => {
        console.error('加载学生数据失败:', error);
        this.loading = false;
      }
    });
  }

  applyFilter(): void {
    this.dataSource.filter = this.searchTerm.trim().toLowerCase();
  }

  openCreateDialog(): void {
    const dialogRef = this.dialog.open(CreateStudentDialogComponent, {
      width: '400px'
    });

    dialogRef.afterClosed().subscribe((result: Student) => {
      if (result) {
        this.createStudent(result);
      }
    });
  }

  createStudent(student: any): void {
    this.adminService.createStudent(student).subscribe({
      next: (newStudent) => {
        // 添加新学生到数据源
        this.students.push(newStudent);
        this.dataSource.data = [...this.students];
        console.log('学生创建成功:', newStudent);
      },
      error: (error) => {
        console.error('创建学生失败:', error);
      }
    });
  }

  editStudent(student: Student): void {
    // TODO: 打开编辑学生对话框
    console.log('编辑学生:', student);
  }

  deleteStudent(studentId: string): void {
    // TODO: 删除学生
    console.log('删除学生:', studentId);
  }
}