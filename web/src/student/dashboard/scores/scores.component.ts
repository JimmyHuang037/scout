import { Component, Input, ViewChild, AfterViewInit } from '@angular/core';
import { Score } from '../../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatPaginatorModule, MatPaginator } from '@angular/material/paginator';
import { MatTableDataSource } from '@angular/material/table';

@Component({
  selector: 'app-scores',
  standalone: true,
  imports: [
    MatCardModule,
    MatTableModule,
    MatProgressSpinnerModule,
    MatPaginatorModule
  ],
  template: `
    <mat-card class="section">
      <mat-card-header>
        <mat-card-title>成绩列表</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="table-container">
          <table mat-table [dataSource]="dataSource" class="data-table">
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
          
          <mat-paginator [pageSize]="5" [pageSizeOptions]="[5, 10, 20]" showFirstLastButtons />
        </div>
        
        @if (loading) {
          <div class="loading-shade">
            <mat-spinner diameter="40"></mat-spinner>
          </div>
        }
        
        @if (!loading && scores.length === 0) {
          <p class="no-data">暂无成绩记录</p>
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
      position: relative;
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
  
  displayedColumns: string[] = ['subject_name', 'exam_name', 'score'];
  dataSource: MatTableDataSource<Score> = new MatTableDataSource<Score>();
  
  @ViewChild(MatPaginator) paginator!: MatPaginator;
  
  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
  }
  
  ngOnChanges() {
    // 当scores数据发生变化时更新dataSource
    this.dataSource.data = this.scores;
  }
}