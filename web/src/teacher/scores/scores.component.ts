import { Component, Input, Output, EventEmitter, OnChanges, SimpleChanges } from '@angular/core';
import { StudentScore } from '../../shared/models';
import { MatCardModule } from '@angular/material/card';
import { MatTableModule, MatTableDataSource } from '@angular/material/table';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';

@Component({
  selector: 'app-teacher-scores',
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatTableModule,
    MatProgressSpinnerModule,
    FormsModule,
    MatInputModule,
    MatButtonModule
  ],
  template: `
    <mat-card class="scores-card">
      <mat-card-header>
        <mat-card-title>学生成绩管理</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        <div class="table-container">
          <table mat-table [dataSource]="dataSource" class="scores-table" mat-table-recycle-rows>
            <ng-container matColumnDef="student_number">
              <th mat-header-cell *matHeaderCellDef>学号</th>
              <td mat-cell *matCellDef="let score">{{ score.student_number }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="student_name">
              <th mat-header-cell *matHeaderCellDef>学生姓名</th>
              <td mat-cell *matCellDef="let score">{{ score.student_name }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="class_name">
              <th mat-header-cell *matHeaderCellDef>班级</th>
              <td mat-cell *matCellDef="let score">{{ score.class_name }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="subject_name">
              <th mat-header-cell *matHeaderCellDef>科目</th>
              <td mat-cell *matCellDef="let score">{{ score.subject_name }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="exam_name">
              <th mat-header-cell *matHeaderCellDef>考试名称</th>
              <td mat-cell *matCellDef="let score">{{ score.exam_name }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="score">
              <th mat-header-cell *matHeaderCellDef>成绩</th>
              <td mat-cell *matCellDef="let score">{{ score.score }}</td>
              <td mat-footer-cell *matFooterCellDef></td>
            </ng-container>

            <ng-container matColumnDef="actions">
              <th mat-header-cell *matHeaderCellDef>操作</th>
              <td mat-cell *matCellDef="let score">
                <div class="score-input-container">
                  <input 
                    [(ngModel)]="scoreInputs[score.score_id]"
                    type="number" 
                    min="0" 
                    max="100" 
                    matInput 
                    placeholder="新成绩"
                    class="score-input">
                  <button 
                    mat-raised-button 
                    color="primary" 
                    (click)="updateScore(score.score_id, scoreInputs[score.score_id])"
                    [disabled]="!scoreInputs[score.score_id] || scoreInputs[score.score_id] < 0 || scoreInputs[score.score_id] > 100"
                    class="update-button">
                    更新
                  </button>
                </div>
              </td>
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
    .scores-card {
      margin-bottom: 20px;
    }
    
    .table-container {
      overflow: auto;
      position: relative;
      max-height: 500px;
    }
    
    .scores-table {
      width: 100%;
    }
    
    .scores-table th,
    .scores-table td {
      padding: 8px 12px;
      text-align: center;
    }
    
    .score-input-container {
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .score-input {
      width: 80px;
    }
    
    .update-button {
      min-width: 60px;
    }
    
    .no-data {
      text-align: center;
      color: #666;
      font-style: italic;
      padding: 20px;
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
export class TeacherScoresComponent implements OnChanges {
  @Input() scores: StudentScore[] = [];
  @Input() loading: boolean = false;
  @Output() scoreUpdate = new EventEmitter<{scoreId: number, newScore: number}>();
  
  dataSource = new MatTableDataSource<StudentScore>();
  scoreInputs: {[key: number]: number} = {};
  displayedColumns: string[] = ['student_number', 'student_name', 'class_name', 'subject_name', 'exam_name', 'score', 'actions'];
  
  ngOnChanges(changes: SimpleChanges): void {
    if (changes['scores'] && changes['scores'].currentValue) {
      this.dataSource.data = changes['scores'].currentValue;
    }
  }
  
  updateScore(scoreId: number, newScore: number): void {
    if (newScore !== undefined && newScore >= 0 && newScore <= 100) {
      this.scoreUpdate.emit({scoreId, newScore});
      delete this.scoreInputs[scoreId];
    }
  }
}