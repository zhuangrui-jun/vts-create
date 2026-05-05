declare module 'sql.js' {
  interface SqlJsStatic {
    Database: new (data?: ArrayLike<number> | Buffer | null) => Database
  }

  interface Database {
    run(sql: string, params?: any[]): Database
    exec(sql: string, params?: any[]): QueryExecResult[]
    prepare(sql: string): Statement
    export(): Uint8Array
    close(): void
  }

  interface QueryExecResult {
    columns: string[]
    values: any[][]
  }

  interface Statement {
    bind(params?: any[]): boolean
    step(): boolean
    getAsObject(): Record<string, any>
    get(): any[]
    free(): void
  }

  interface InitOptions {
    locateFile?: (file: string) => string
  }

  export default function initSqlJs(options?: InitOptions): Promise<SqlJsStatic>
  export type { SqlJsStatic, Database, QueryExecResult, Statement, InitOptions }
}
