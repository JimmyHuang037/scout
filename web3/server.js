const express = require('express');
const mysql = require('mysql2');
const path = require('path');

const app = express();
const port = 3000;

// 创建MySQL连接池
const dbConfig = {
    host: 'localhost',
    user: 'root',
    password: 'Newuser1',
    database: 'school_management'
};

const pool = mysql.createPool(dbConfig);

// 提供静态文件服务（HTML, CSS, JS）
app.use(express.static(path.join(__dirname)));

// API端点：获取所有教师数据
app.get('/api/teachers', (req, res) => {
    const query = 'SELECT * FROM Teachers';
    
    pool.query(query, (error, results) => {
        if (error) {
            console.error('数据库查询错误:', error);
            res.status(500).json({ error: '数据库查询失败' });
            return;
        }
        
        res.json(results);
    });
});

// API端点：根据ID获取特定教师
app.get('/api/teachers/:id', (req, res) => {
    const teacherId = req.params.id;
    const query = 'SELECT * FROM Teachers WHERE id = ?';
    
    pool.query(query, [teacherId], (error, results) => {
        if (error) {
            console.error('数据库查询错误:', error);
            res.status(500).json({ error: '数据库查询失败' });
            return;
        }
        
        if (results.length === 0) {
            res.status(404).json({ error: '未找到指定的教师' });
            return;
        }
        
        res.json(results[0]);
    });
});

// 启动服务器
app.listen(port, () => {
    console.log(`服务器运行在 http://localhost:${port}`);
    console.log('请在浏览器中打开此地址以查看应用');
});

module.exports = app;