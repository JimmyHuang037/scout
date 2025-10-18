import { Component, OnInit } from '@angular/core';
import { StudentService } from '../student.service';
import { Student, Score, ExamResult } from '../student.model';
import { MatTableModule } from '@angular/material/table';
import { MatCardModule } from '@angular/material/card';
import { MatTabsModule } from '@angular/material/tabs';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [
    MatTableModule,
    MatCardModule,
    MatTabsModule,
    CommonModule
  ],
  template: `
    <div class="dashboard-container">
      <mat-card>
        <mat-card-header>
          <mat-card-title>学生信息</mat-card-title>
        </mat-card-header>
        <mat-card-content>
          <div *ngIf="studentProfile; else noProfile">
            <p><strong>学号:</strong> {{ studentProfile.student_id }}</p>
            <p><strong>姓名:</strong> {{ studentProfile.student_name }}</p>
            <p><strong>班级:</strong> {{ studentProfile.class_name }}</p>
          </div>
          <ng-template #noProfile>
            <p>加载中...</p>
          </ng-template>
        </mat-card-content>
      </mat-card>

      <mat-tab-group>
        <mat-tab label="成绩">
          <div *ngIf="scores.length > 0; else noScores">
            <table mat-table [dataSource]="scores" class="mat-elevation-z8">
              <ng-container matColumnDef="exam_name">
                <th mat-header-cell *matHeaderCellDef>考试类型</th>
                <td mat-cell *matCellDef="let score">{{ score.exam_name }}</td>
              </ng-container>

              <ng-container matColumnDef="subject_name">
                <th mat-header-cell *matHeaderCellDef>科目</th>
                <td mat-cell *matCellDef="let score">{{ score.subject_name }}</td>
              </ng-container>

              <ng-container matColumnDef="score">
                <th mat-header-cell *matHeaderCellDef>分数</th>
                <td mat-cell *matCellDef="let score">{{ score.score }}</td>
              </ng-container>

              <tr mat-header-row *matHeaderRowDef="displayedScoreColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: displayedScoreColumns;"></tr>
            </table>
          </div>
          <ng-template #noScores>
            <p>暂无成绩数据</p>
          </ng-template>
        </mat-tab>

        <mat-tab label="考试结果">
          <div *ngIf="examResults.length > 0; else noResults">
            <table mat-table [dataSource]="examResults" class="mat-elevation-z8">
              <ng-container matColumnDef="exam_name">
                <th mat-header-cell *matHeaderCellDef>考试名称</th>
                <td mat-cell *matCellDef="let result">{{ result.exam_name }}</td>
              </ng-container>

              <ng-container matColumnDef="chinese">
                <th mat-header-cell *matHeaderCellDef>语文</th>
                <td mat-cell *matCellDef="let result">{{ result.chinese }}</td>
              </ng-container>

              <ng-container matColumnDef="math">
                <th mat-header-cell *matHeaderCellDef>数学</th>
                <td mat-cell *matCellDef="let result">{{ result.math }}</td>
              </ng-container>

              <ng-container matColumnDef="english">
                <th mat-header-cell *matHeaderCellDef>英语</th>
                <td mat-cell *matCellDef="let result">{{ result.english }}</td>
              </ng-container>

              <ng-container matColumnDef="physics">
                <th mat-header-cell *matHeaderCellDef>物理</th>
                <td mat-cell *matCellDef="let result">{{ result.physics }}</td>
              </ng-container>

              <ng-container matColumnDef="chemistry">
                <th mat-header-cell *matHeaderCellDef>化学</th>
                <td mat-cell *matCellDef="let result">{{ result.chemistry }}</td>
              </ng-container>

              <ng-container matColumnDef="politics">
                <th mat-header-cell *matHeaderCellDef>政治</th>
                <td mat-cell *matCellDef="let result">{{ result.politics }}</td>
              </ng-container>

              <ng-container matColumnDef="total_score">
                <th mat-header-cell *matHeaderCellDef>总分</th>
                <td mat-cell *matCellDef="let result">{{ result.total_score }}</td>
              </ng-container>

              <ng-container matColumnDef="ranking">
                <th mat-header-cell *matHeaderCellDef>排名</th>
                <td mat-cell *matCellDef="let result">{{ result.ranking }}</td>
              </ng-container>

              <tr mat-header-row *matHeaderRowDef="displayedResultColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: displayedResultColumns;"></tr>
            </table>
          </div>
          <ng-template #noResults>
            <p>暂无考试结果数据</p>
          </ng-template>
        </mat-tab>
      </mat-tab-group>
      
      <div *ngIf="errorMessages.length > 0" class="error-container">
        <h3>错误信息:</h3>
        <ul>
          <li *ngFor="let error of errorMessages">{{ error }}</li>
        </ul>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
    }
    
    mat-card {
      margin-bottom: 20px;
    }
    
    table {
      width: 100%;
    }
    
    mat-tab-group {
      margin-top: 20px;
    }
    
    .error-container {
      margin-top: 20px;
      padding: 10px;
      background-color: #ffebee;
      border: 1px solid #f44336;
      border-radius: 4px;
    }
  `]
})
export class DashboardComponent implements OnInit {
  studentProfile: Student | null = null;
  scores: Score[] = [];
  examResults: ExamResult[] = [];
  errorMessages: string[] = [];
  
  displayedScoreColumns: string[] = ['exam_name', 'subject_name', 'score'];
  displayedResultColumns: string[] = ['exam_name', 'chinese', 'math', 'english', 'physics', 'chemistry', 'politics', 'total_score', 'ranking'];
  
  constructor(private studentService: StudentService) { }
  
  ngOnInit(): void {
    // 使用默认学生ID S0101 进行演示
    this.loadStudentData('S0101');
  }
  
  loadStudentData(studentId: string): void {
    console.log('开始加载学生数据，学生ID:', studentId);
    
    this.studentService.getStudentProfile(studentId).subscribe({
      next: (profile) => {
        console.log('获取到学生个人资料:', profile);
        this.studentProfile = profile;
      },
      error: (error) => {
        console.error('获取学生个人资料出错:', error);
        this.errorMessages.push('获取学生个人资料出错: ' + JSON.stringify(error));
      }
    });
    
    this.studentService.getStudentScores(studentId).subscribe({
      next: (scores) => {
        console.log('获取到学生成绩:', scores);
        this.scores = scores;
      },
      error: (error) => {
        console.error('获取学生成绩出错:', error);
        this.errorMessages.push('获取学生成绩出错: ' + JSON.stringify(error));
      }
    });
    
    this.studentService.getStudentExamResults(studentId).subscribe({
      next: (results) => {
        console.log('获取到考试结果:', results);
        this.examResults = results;
      },
      error: (error) => {
        console.error('获取考试结果出错:', error);
        this.errorMessages.push('获取考试结果出错: ' + JSON.stringify(error));
      }
    });
  }
}