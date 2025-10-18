import { Component, Input } from '@angular/core';
import { Score } from '../../../shared/models';
import { NgIf } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [
    NgIf, 
    MatCardModule,
    MatTableModule,
    MatProgressSpinnerModule
  ],
  template: `
    <mat-card class="section">
      <mat-card-header>
        <mat-card-title>成绩列表</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="table-container" *ngIf="scores.length > 0; else noData">
          <table mat-table [dataSource]="scores" class="data-table">
            <ng-container matColumnDef="subject_name">
              <th mat-header-cell *matHeaderCellDef>科目</th>
              <td mat-cell *matCellDef="let score">{{score.subject_name}}</td>
            </ng-container>

            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef>考试类型</th>
              <td mat-cell *matCellDef="let score">{{score.exam_name}}</td>
            </ng-container>

            <ng-container matColumnDef="score">
              <th mat-header-cell *matHeaderCellDef>分数</th>
              <td mat-cell *matCellDef="let score">{{score.score}}</td>
            </ng-container>

            <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
            <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
          </table>
        </div>
        
        <ng-template #noData>
          <mat-spinner *ngIf="loading" diameter="40"></mat-spinner>
          <p *ngIf="!loading" class="no-data">暂无成绩记录</p>
        </ng-template>
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
export class ScoresComponent {
  @Input() scores: Score[] = [];
  @Input() loading: boolean = false;
  
  displayedColumns: string[] = ['subject_name', 'exam_name', 'score'];
}