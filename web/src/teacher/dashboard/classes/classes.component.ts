import { Component, Input, ViewChild, AfterViewInit } from '@angular/core';
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

@Component({
  selector: 'app-classes',
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
    CommonModule
  ],
  template: `
    <mat-card class="classes-card">
      <mat-card-header>
        <mat-card-title>班级管理</mat-card-title>
      </mat-card-header>
      <mat-card-content>
        @if (loading) {
          <div class="loading-container">
            <mat-spinner diameter="30"></mat-spinner>
            <span>加载中...</span>
          </div>
        } @else {
          <div class="classes-table-container">
            <mat-form-field class="search-field">
              <mat-label>搜索</mat-label>
              <input matInput (keyup)="applyFilter($event)" placeholder="输入关键词进行搜索" #input>
            </mat-form-field>
            
            <table mat-table [dataSource]="dataSource" matSort>
              <!-- 班级ID列 -->
              <ng-container matColumnDef="class_id">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>班级ID</th>
                <td mat-cell *matCellDef="let element">{{element.class_id}}</td>
              </ng-container>

              <!-- 班级名称列 -->
              <ng-container matColumnDef="class_name">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>班级名称</th>
                <td mat-cell *matCellDef="let element">{{element.class_name}}</td>
              </ng-container>

              <!-- 班主任列 -->
              <ng-container matColumnDef="teacher_name">
                <th mat-header-cell *matHeaderCellDef mat-sort-header>班主任</th>
                <td mat-cell *matCellDef="let element">{{element.teacher_name}}</td>
              </ng-container>

              <tr mat-header-row *matHeaderRowDef="displayedColumns"></tr>
              <tr mat-row *matRowDef="let row; columns: displayedColumns;"></tr>
            </table>

            <mat-paginator 
              [pageSizeOptions]="[5, 10, 20]" 
              showFirstLastButtons 
              aria-label="选择页面">
            </mat-paginator>
          </div>
        }
      </mat-card-content>
    </mat-card>
  `,
  styles: [`
    .classes-card {
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
    .classes-table-container {
      overflow-x: auto;
    }
    table {
      width: 100%;
    }
    .mat-mdc-table .mat-mdc-row:hover {
      background-color: #f5f5f5;
    }
  `]
})
export class ClassesComponent implements AfterViewInit {
  @Input() loading: boolean = false;
  @Input() set classes(classes: any[]) {
    this.dataSource.data = classes;
  }

  displayedColumns: string[] = ['class_id', 'class_name', 'teacher_name'];
  dataSource = new MatTableDataSource<any>();

  @ViewChild(MatPaginator) paginator!: MatPaginator;
  @ViewChild(MatSort) sort!: MatSort;

  ngAfterViewInit() {
    this.dataSource.paginator = this.paginator;
    this.dataSource.sort = this.sort;
  }

  applyFilter(event: Event) {
    const filterValue = (event.target as HTMLInputElement).value;
    this.dataSource.filter = filterValue.trim().toLowerCase();

    if (this.dataSource.paginator) {
      this.dataSource.paginator.firstPage();
    }
  }
}