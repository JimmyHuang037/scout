import { Component, Input, ViewChild, AfterViewInit, OnDestroy, OnChanges, SimpleChanges, Output, EventEmitter } from '@angular/core';
import { StudentScore } from '../../../shared/models';
import { MatTableModule } from '@angular/material/table';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { CommonModule } from '@angular/common';
import { MatIconModule } from '@angular/material/icon';
import { MatButtonModule } from '@angular/material/button';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { MatInputModule as MatInput } from '@angular/material/input';
import { MatSnackBar, MatSnackBarModule } from '@angular/material/snack-bar';

interface ScoreUpdateEvent {
  teacherId: number;
  scoreId: number;
  score: number;
}

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [
    MatTableModule,
    MatPaginatorModule,
    MatSortModule,
    MatCardModule,
    MatProgressSpinnerModule,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    CommonModule,
    MatIconModule,
    MatButtonModule,
    MatDialogModule,
    MatInput,
    MatSnackBarModule
  ],
  template: `
    <mat-card class="scores-card">
      <mat-card-header>
        <mat-card-title>成绩管理</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="loading-container" *ngIf="loading">
          <mat-spinner diameter="30"></mat-spinner>
          <span>加载中...</span>
        </div>
        
        <!-- 始终渲染表格和分页器，避免使用@if指令包裹 -->
        <div class="scores-table-container">
          <mat-form-field class="search-field">
            <mat-label>搜索</mat-label>
            <input matInput (keyup)="applyFilter($event)" placeholder="输入关键词进行搜索" #input>
          </mat-form-field>
          
          <table mat-table [dataSource]="dataSource" matSort>
            <!-- 成绩ID列 -->
            <ng-container matColumnDef="score_id">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>成绩ID</th>
              <td mat-cell *matCellDef="let element">{{element.score_id}}</td>
            </ng-container>

            <!-- 学生学号列 -->
            <ng-container matColumnDef="student_number">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>学生学号</th>
              <td mat-cell *matCellDef="let element">{{element.student_number}}</td>
            </ng-container>

            <!-- 学生姓名列 -->
            <ng-container matColumnDef="student_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>学生姓名</th>
              <td mat-cell *matCellDef="let element">{{element.student_name}}</td>
            </ng-container>

            <!-- 科目名称列 -->
            <ng-container matColumnDef="subject_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>科目</th>
              <td mat-cell *matCellDef="let element">{{element.subject_name}}</td>
            </ng-container>

            <!-- 考试名称列 -->
            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>考试名称</th>
              <td mat-cell *matCellDef="let element">{{element.exam_name}}</td>
            </ng-container>

            <!-- 分数列 -->
            <ng-container matColumnDef="score">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>分数</th>
              <td mat-cell *matCellDef="let element">
                <span *ngIf="!isEditing(element.score_id)">{{element.score}}</span>
                <mat-form-field *ngIf="isEditing(element.score_id)" class="score-input">
                  <input matInput type="number" [(ngModel)]="editingScore" min="0" max="100">
                </mat-form-field>
              </td>
            </ng-container>

            <!-- 操作列 -->
            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let element">
                <button *ngIf="!isEditing(element.score_id)" mat-icon-button (click)="startEdit(element.score_id, element.score)">
                  <mat-icon>edit</mat-icon>
                </button>
                <button *ngIf="isEditing(element.score_id)" mat-icon-button (click)="saveScore(element.score_id)">
                  <mat-icon>save</mat-icon>
                </button>
                <button *ngIf="isEditing(element.score_id)" mat-icon-button (click)="cancelEdit()">
                  <mat-icon>cancel</mat-icon>
                </button>
              </td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>

          <mat-paginator 
            [pageSizeOptions]="[5, 10, 20, 50]" 
            [pageSize]="10"
            showFirstLastButtons 
            aria-label="选择页面">
          </mat-paginator>
        </div>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .scores-card {
      margin-bottom: 16px;
    }
    .loading-container {
      display: flex;
      align-items: center;
      justify-content: center;
      padding: 20px;
      gap: 10px;
    }
    .search-field {
      width: 100%;
      margin-bottom: 16px;
    }
    .scores-table-container {
      overflow-x: auto;
    }
    table {
      width: 100%;
    }
    .mat-mdc-table .mat-mdc-row:hover {
      background-color: #f5f5f5;
    }
    .score-input {
      width: 80px;
    }
  `]
})
export class ScoresComponent implements AfterViewInit, OnDestroy, OnChanges {
  @Input() loading: boolean = false;
  @Input() scores: StudentScore[] = [];
  @Input() teacherId: number = 0;
  @Output() scoreUpdated = new EventEmitter<ScoreUpdateEvent>();

  displayedColumns: string[] = ['score_id', 'student_number', 'student_name', 
                               'subject_name', 'exam_name', 'score', 'actions'];
  dataSource = new MatTableDataSource<StudentScore>();

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  // 编辑状态管理
  editingScoreId: number | null = null;
  editingScore: number = 0;
  originalScore: number = 0;

  constructor(
    private snackBar: MatSnackBar
  ) {}

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['scores'] && changes['scores'].currentValue) {
      this.dataSource.data = changes['scores'].currentValue;
    }
  }

  ngOnDestroy() {
    // Clean up data source to prevent memory leaks
    this.dataSource.disconnect();
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }

  // 编辑功能相关方法
  isEditing(scoreId: number): boolean {
    return this.editingScoreId === scoreId;
  }

  startEdit(scoreId: number, score: number): void {
    this.editingScoreId = scoreId;
    this.editingScore = score;
    this.originalScore = score;
  }

  cancelEdit(): void {
    this.editingScoreId = null;
    this.editingScore = 0;
  }

  saveScore(scoreId: number): void {
    if (this.teacherId && this.editingScoreId) {
      this.scoreUpdated.emit({
        teacherId: this.teacherId,
        scoreId: this.editingScoreId,
        score: this.editingScore
      });
      // 不再立即清除编辑状态，而是在父组件更新成功后通过@Input更新
    }
  }
}