import { Component, Input } from '@angular/core';
import { ExamResult } from '../../../shared/models';
import { NgIf, NgFor } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-exams',
  standalone: true,
  imports: [
    NgIf, 
    NgFor,
    MatCardModule,
    MatTableModule,
    MatProgressSpinnerModule
  ],
  template: `
    <mat-card class="section">
      <mat-card-header>
        <mat-card-title>考试结果</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="table-container" *ngIf="examResults.length > 0; else noData">
          <table mat-table [dataSource]="examResults" class="data-table">
            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef>考试名称</th>
              <td mat-cell *matCellDef="let result">{{result.exam_name}}</td>
            </ng-container>

            <ng-container matColumnDef="chinese">
              <th mat-header-cell *matHeaderCellDef>语文</th>
              <td mat-cell *matCellDef="let result">{{result.chinese}}</td>
            </ng-container>

            <ng-container matColumnDef="math">
              <th mat-header-cell *matHeaderCellDef>数学</th>
              <td mat-cell *matCellDef="let result">{{result.math}}</td>
            </ng-container>

            <ng-container matColumnDef="english">
              <th mat-header-cell *matHeaderCellDef>英语</th>
              <td mat-cell *matCellDef="let result">{{result.english}}</td>
            </ng-container>

            <ng-container matColumnDef="physics">
              <th mat-header-cell *matHeaderCellDef>物理</th>
              <td mat-cell *matCellDef="let result">{{result.physics}}</td>
            </ng-container>

            <ng-container matColumnDef="chemistry">
              <th mat-header-cell *matHeaderCellDef>化学</th>
              <td mat-cell *matCellDef="let result">{{result.chemistry}}</td>
            </ng-container>

            <ng-container matColumnDef="politics">
              <th mat-header-cell *matHeaderCellDef>政治</th>
              <td mat-cell *matCellDef="let result">{{result.politics}}</td>
            </ng-container>

            <ng-container matColumnDef="total_score">
              <th mat-header-cell *matHeaderCellDef>总分</th>
              <td mat-cell *matCellDef="let result">{{result.total_score}}</td>
            </ng-container>

            <ng-container matColumnDef="ranking">
              <th mat-header-cell *matHeaderCellDef>排名</th>
              <td mat-cell *matCellDef="let result">{{result.ranking}}</td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>
        </div>
        
        <ng-template #noData>
          <div class="no-data" *ngIf="!loading">
            <p>暂无考试结果</p>
          </div>
          <div class="loading" *ngIf="loading">
            <mat-spinner diameter="30"></mat-spinner>
            <p>加载中...</p>
          </div>
        </ng-template>
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .section {
      margin-bottom: 30px;
    }

    .table-container {
      overflow-x: auto;
    }

    .data-table {
      width: 100%;
      margin-top: 10px;
    }

    .no-data, .loading {
      text-align: center;
      padding: 20px;
    }

    .loading {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    mat-spinner {
      margin-bottom: 10px;
    }
  `]
})
export class ExamsComponent {
  @Input() examResults: ExamResult[] = [];
  @Input() loading: boolean = false;
  
  displayedColumns: string[] = ['exam_name', 'chinese', 'math', 'english', 'physics', 'chemistry', 'politics', 'total_score', 'ranking'];
}