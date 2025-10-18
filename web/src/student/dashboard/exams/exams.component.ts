import { Component, Input } from '@angular/core';
import { ExamResult } from '../../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-exams',
  standalone: true,
  imports: [
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
        @if (examResults.length > 0) {
          <div class="table-container">
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

              <ng-container matColumnDef="total">
                <th mat-header-cell *matHeaderCellDef>总分</th>
                <td mat-cell *matCellDef="let result">{{result.total}}</td>
              </ng-container>

              <ng-container matColumnDef="average">
                <th mat-header-cell *matHeaderCellDef>平均分</th>
                <td mat-cell *matCellDef="let result">{{result.average}}</td>
              </ng-container>

              <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
            </table>
          </div>
        } @else {
          @if (loading) {
            <mat-spinner diameter="40"></mat-spinner>
          } @else {
            <p class="no-data">暂无考试结果</p>
          }
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .section {
      margin-bottom: 20px;
    }
    
    .table-container {
      overflow-x: auto;
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
    
    .no-data {
      text-align: center;
      color: #666;
      font-style: italic;
      padding: 20px;
    }
  `]
})
export class ExamsComponent {
  @Input() examResults: ExamResult[] = [];
  @Input() loading = false;
  
  displayedColumns: string[] = ['exam_name', 'chinese', 'math', 'english', 'total', 'average'];
}