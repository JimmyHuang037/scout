import { Component, Input } from '@angular/core';
import { ExamResult } from '../../shared/student.model';
import { NgIf, NgFor } from '@angular/common';

@Component({
  selector: 'app-exams',
  standalone: true,
  imports: [NgIf, NgFor],
  template: `
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
  `,
  styles: [`
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
export class ExamsComponent {
  @Input() examResults: ExamResult[] = [];
  @Input() loading: boolean = false;
}