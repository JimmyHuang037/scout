import { Component, Input, ViewChild, AfterViewInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Score } from '../../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatSortModule, MatSort } from '@angular/material/sort';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatSortModule,
    MatProgressSpinnerModule
  ],
  template: `
    <mat-card class="section">
      <mat-card-header>
        <mat-card-title>成绩列表</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="table-container">
          <table mat-table [dataSource]="dataSource" class="data-table" mat-table-recycle-rows matSort>
            <!-- 新增两列: score_id 和 student_name -->
            <ng-container matColumnDef="score_id">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>编号</th>
              <td mat-cell *matCellDef="let score">{{score.score_id}}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="student_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>学生</th>
              <td mat-cell *matCellDef="let score">{{score.student_name}}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>
            <ng-container matColumnDef="subject_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>科目</th>
              <td mat-cell *matCellDef="let score">{{score.subject_name}}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>考试类型</th>
              <td mat-cell *matCellDef="let score">{{score.exam_name}}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="score">
              <th mat-header-cell *matHeaderCellDef mat-sort-header>分数</th>
              <td mat-cell *matCellDef="let score">{{score.score}}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>
        </div>
        
        <div *ngIf="loading" class="loading-shade">
          <mat-spinner diameter="40"></mat-spinner>
        </div>

        <p *ngIf="!loading && scores.length === 0" class="no-data">暂无成绩记录</p>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .section {
      margin-bottom: 20px;
    }
    
    .table-container {
      overflow: auto;
      position: relative;
      height: 300px;
    }
    
    .data-table {
      width: 100%;
      table-layout: fixed;
    }
    
    .data-table th,
    .data-table td {
      padding: 8px;
      text-align: center;
    }

    /* 鼠标悬停时高亮整行（提高优先级并兼容 tr[mat-row]） */
    .data-table tr.mat-row:hover,
    .data-table tr[mat-row]:hover {
      cursor: pointer;
    }

    /* 把高亮颜色应用到每个单元格，使用 !important 避免被主题覆盖 */
    .data-table tr.mat-row:hover td,
    .data-table tr[mat-row]:hover td {
      /* 黄色高亮（稍透明以保留表格可读性） */
      background-color: rgba(255, 235, 59, 0.25) !important;
      transition: background-color 150ms ease-in;
    }
    
    .no-data {
      text-align: center;
      color: #666;
      font-style: italic;
      padding: 20px;
    }
    
    mat-paginator {
      margin-top: 10px;
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
  `]
})
export class ScoresComponent implements AfterViewInit {
  @Input() scores: Score[] = [];
  @Input() loading: boolean = false;

  @ViewChild(MatSort) sort!: MatSort;
  
  displayedColumns: string[] = ['score_id', 'student_name', 'subject_name', 'exam_name', 'score'];
  dataSource: MatTableDataSource<Score> = new MatTableDataSource<Score>();
  
  ngOnChanges() {
    // 当scores数据发生变化时更新dataSource
    this.dataSource.data = this.scores;
    // 如果 sort 已经初始化，确保 dataSource 使用它
    if (this.sort) {
      this.dataSource.sort = this.sort;
    }
  }

  ngAfterViewInit(): void {
    // 在视图初始化后连接排序
    this.dataSource.sort = this.sort;
  }
}