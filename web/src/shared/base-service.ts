import { HttpClient, HttpErrorResponse } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, map, retryWhen, delay, take, concatMap } from 'rxjs/operators';

// 定义API响应接口
export interface ApiResponse<T> {
  data: T;
  message: string;
  success: boolean;
  timestamp: string;
}

export abstract class BaseService {
  protected baseUrl: string = '';
  
  constructor(protected http: HttpClient) {}

  protected handleError = (error: HttpErrorResponse | Error): Observable<never> => {
    let errorMessage = '';
    
    if (error instanceof HttpErrorResponse) {
      if (error.error instanceof ErrorEvent) {
        // 客户端错误
        errorMessage = `客户端错误: ${error.error.message}`;
      } else {
        // 服务器端错误
        errorMessage = `服务器返回代码 ${error.status}: ${error.message}`;
      }
    } else {
      // 解析错误或其他错误
      errorMessage = `解析错误: ${error.message}`;
    }
    
    console.error(errorMessage);
    // 返回错误信息而不是抛出错误，这样组件可以显示错误但不会中断其他请求
    return throwError(() => errorMessage);
  }

  protected transformToNumber(value: any): number {
    return Number(value);
  }

  /**
   * 通用对象字段转换方法
   * @param obj 要转换的对象
   * @param numericFields 需要转换为数字的字段名数组
   */
  protected transformObjectFields<T>(obj: any, numericFields: string[]): T {
    const result: any = { ...obj };
    numericFields.forEach(field => {
      if (result[field] !== undefined) {
        result[field] = this.transformToNumber(result[field]);
      }
    });
    return result;
  }

  /**
   * 获取数据列表的通用方法
   */
  protected getList<T>(endpoint: string): Observable<T[]> {
    return this.http.get<ApiResponse<T[]>>(`${this.baseUrl}/${endpoint}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  /**
   * 获取单个数据的通用方法
   */
  protected getOne<T>(endpoint: string): Observable<T> {
    return this.http.get<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  /**
   * 处理返回文本格式的API响应
   */
  protected getTextResponse<T>(endpoint: string): Observable<T[]> {
    return this.http.get(`${this.baseUrl}/${endpoint}`, { responseType: 'text' })
      .pipe(
        map(response => {
          // 检查响应是否为HTML（错误页面）
          if (response.startsWith('<!doctype') || response.startsWith('<html')) {
            throw new Error('Received HTML response instead of JSON. Check if the API server is running and the endpoint is correct.');
          }
          
          // 解析JSON响应
          const parsedResponse: ApiResponse<any[]> = JSON.parse(response);
          return parsedResponse.data;
        }),
        catchError(this.handleError)
      );
  }

  /**
   * 获取可能有Content-Type问题的JSON数据
   */
  protected getJsonWithFallback<T>(endpoint: string): Observable<T[]> {
    return this.http.get<ApiResponse<T[]>>(`${this.baseUrl}/${endpoint}`)
      .pipe(
        map(response => response.data),
        catchError((error: HttpErrorResponse) => {
          // 如果是解析错误，尝试用文本方式获取
          if (error.status === 200 && error.statusText === 'OK') {
            // 可能是Content-Type问题，尝试文本方式获取
            return this.getTextResponse<T>(endpoint);
          }
          throw error;
        }),
        catchError(this.handleError)
      );
  }

  /**
   * 通用POST请求方法
   */
  protected post<T>(endpoint: string, body: any): Observable<T> {
    return this.http.post<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`, body)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  /**
   * 通用PUT请求方法
   */
  protected put<T>(endpoint: string, body: any): Observable<T> {
    return this.http.put<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`, body)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }

  /**
   * 通用DELETE请求方法
   */
  protected delete<T>(endpoint: string): Observable<T> {
    return this.http.delete<ApiResponse<T>>(`${this.baseUrl}/${endpoint}`)
      .pipe(
        map(response => response.data),
        catchError(this.handleError)
      );
  }
}