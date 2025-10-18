import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { StudentService } from '../../shared/services';
import { Student, Score, ExamResult } from '../../shared/models';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [NgIf, NgFor],
  template: `
    <div class="dashboard-container" *ngIf="studentId">
      <div class="welcome-section">
        <h2>欢迎, {{student?.student_name}}!</h2>
        <p>学号: {{student?.student_id}}</p>
        <p>班级: {{student?.class_name}}</p>
      </div>

      <div class="section">
        <h3>个人信息</h3>
        <div class="info-grid" *ngIf="student">
          <div class="info-item">
            <span class="label">姓名:</span>
            <span>{{student.student_name}}</span>
          </div>
          <div class="info-item">
            <span class="label">学号:</span>
            <span>{{student.student_id}}</span>
          </div>
          <div class="info-item">
            <span class="label">班级:</span>
            <span>{{student.class_name}}</span>
          </div>
        </div>
      </div>

      <div class="section">
        <h3>成绩列表</h3>
        <table class="data-table" *ngIf="scores.length > 0">
          <thead>
            <tr>
              <th>科目</th>
              <th>考试类型</th>
              <th>分数</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let score of scores">
              <td>{{score.subject_name}}</td>
              <td>{{score.exam_name}}</td>
              <td>{{score.score}}</td>
            </tr>
          </tbody>
        </table>
        <p *ngIf="scores.length === 0 && !loading">暂无成绩记录</p>
        <p *ngIf="loading">加载中...</p>
      </div>

      <div class="section">
        <h3>考试结果</h3>
        <table class="data-table" *ngIf="examResults.length > 0">
          <thead>
            <tr>
              <th>考试名称</th>
              <th>语文</th>
              <th>数学</th>
              <th>英语</th>
              <th>物理</th>
              <th>化学</th>
              <th>政治</th>
              <th>总分</th>
              <th>排名</th>
            </tr>
          </thead>
          <tbody>
            <tr *ngFor="let result of examResults">
              <td>{{result.exam_name}}</td>
              <td>{{result.chinese}}</td>
              <td>{{result.math}}</td>
              <td>{{result.english}}</td>
              <td>{{result.physics}}</td>
              <td>{{result.chemistry}}</td>
              <td>{{result.politics}}</td>
              <td>{{result.total_score}}</td>
              <td>{{result.ranking}}</td>
            </tr>
          </tbody>
        </table>
        <p *ngIf="examResults.length === 0 && !loading">暂无考试结果</p>
        <p *ngIf="loading">加载中...</p>
      </div>
    </div>
  `,
  styles: [`
    .dashboard-container {
      padding: 20px;
    }

    .welcome-section {
      background-color: #e3f2fd;
      padding: 20px;
      border-radius: 8px;
      margin-bottom: 30px;
      text-align: center;
    }

    .welcome-section h2 {
      margin: 0 0 10px 0;
      color: #1976d2;
    }

    .section {
      margin-bottom: 30px;
      background: white;
      border-radius: 8px;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      padding: 20px;
    }

    .section h3 {
      margin-top: 0;
      color: #333;
      border-bottom: 2px solid #3f51b5;
      padding-bottom: 10px;
    }

    .info-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
      gap: 15px;
    }

    .info-item {
      display: flex;
      flex-direction: column;
    }

    .label {
      font-weight: bold;
      color: #555;
    }

    .data-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 10px;
    }

    .data-table th,
    .data-table td {
      padding: 12px;
      text-align: left;
      border-bottom: 1px solid #ddd;
    }

    .data-table th {
      background-color: #f5f5f5;
      font-weight: bold;
      color: #333;
    }

    .data-table tbody tr:hover {
      background-color: #f9f9f9;
    }

    .data-table tbody tr:last-child td {
      border-bottom: none;
    }
  `]
})
export class DashboardComponent implements OnInit {
  studentId: string | null = null;
  
  student: Student | null = null;
  scores: Score[] = [];
  examResults: ExamResult[] = [];
  loading = false;

  constructor(
    private studentService: StudentService,
    private route: ActivatedRoute
  ) {}

  ngOnInit(): void {
    this.route.queryParams.subscribe(params => {
      this.studentId = params['studentId'] || null;
      if (this.studentId) {
        this.loadStudentData();
      }
    });
  }

  loadStudentData(): void {
    if (!this.studentId) return;
    
    this.loading = true;
    
    // 获取学生个人信息
    this.studentService.getStudentProfile(this.studentId).subscribe({
      next: (student: Student) => {
        this.student = student;
      },
      error: (error: any) => {
        console.error('Error loading student profile:', error);
      }
    });

    // 获取学生成绩
    this.studentService.getStudentScores(this.studentId).subscribe({
      next: (scores: Score[]) => {
        this.scores = scores;
      },
      error: (error: any) => {
        console.error('Error loading student scores:', error);
      }
    });

    // 获取考试结果
    this.studentService.getStudentExamResults(this.studentId).subscribe({
      next: (results: ExamResult[]) => {
        this.examResults = results;
        this.loading = false;
      },
      error: (error: any) => {
        console.error('Error loading exam results:', error);
        this.loading = false;
      }
    });
  }
}