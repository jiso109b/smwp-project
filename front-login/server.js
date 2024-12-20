const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');
const path = require('path');

// Express 서버 설정
const app = express();
const port = 3000;


// CORS 설정 (프론트엔드와의 통신 허용)
app.use(cors({
    origin: '*',  // 또는 정확한 도메인을 넣어서 허용
    methods: ['GET', 'POST'],
    allowedHeaders: ['Content-Type'],
}));

app.use(express.json()); // JSON 요청 본문을 파싱

// 정적 파일 서빙 설정
app.use(express.static('/var/www/html'));  // HTML 파일이 있는 경로

// MySQL 연결 설정
const connection = mysql.createConnection({
    host: 'smwp-apt-rds-db.c9o6gociwe1o.ap-northeast-2.rds.amazonaws.com',   // MySQL 서버 주소
    user: 'smwpuser',    // MySQL 사용자명
    password: 'smwppassword',// MySQL 비밀번호
    database: 'tempDB'   // 데이터베이스 이름
});

//login DB 접속
const connect = mysql.createConnection({
    host: 'smwp-apt-rds-db.c9o6gociwe1o.ap-northeast-2.rds.amazonaws.com',  
    user: 'smwpuser',    
    password: 'smwppassword',
    database: 'user_db'
})


// /login 경로 처리
app.post('/login', (req, res) => {
    const { ID, Password } = req.body;

    if (!ID || !Password) {
        return res.status(400).json({ message: '아이디와 비밀번호를 모두 입력해주세요.' });
    }

    // SQL 쿼리 작성 및 실행
    const query = 'SELECT * FROM users WHERE id = ? AND password = ?';
    connect.query(query, [ID, Password], (err, results) => {
        if (err) {
            console.error('쿼리 실행 오류:', err.message);
            return res.status(500).json({ message: '로그인 요청 중 오류가 발생했습니다.' });
        }

        if (results.length > 0) {
            // 로그인 성공
            res.status(200).json({ message: '로그인 성공' });
        } else {
            // 로그인 실패
            res.status(401).json({ message: '아이디 또는 비밀번호가 틀립니다.' });
        }
    });
});


// API 요청 시 최근 20개의 데이터 반환
app.get('/api/recent', (req, res) => {
    const query = 'SELECT TIME, PV FROM tempDB.tb ORDER BY TIME DESC LIMIT 20';

    connection.query(query, (err, results) => {
        if (err) {
            return res.status(500).send('Database query error');
        }

        res.json(results);
    });
});

// API 요청 시 전체 데이터 반환
app.get('/api/all', (req, res) => {
    const query = 'SELECT TIME, PV FROM tempDB.tb ORDER BY TIME DESC';

    connection.query(query, (err, results) => {
        if (err) {
            return res.status(500).send('Database query error');
        }

        res.json(results);
    });
});

// 최근 1분간의 최대, 평균, 최소 값 반환
app.get('/api/stats', (req, res) => {
    const query = `
        SELECT
            NOW() AS time,
            MAX(PV) AS max,
            AVG(PV) AS avg,
            MIN(PV) AS min
        FROM tempDB.tb
        WHERE TIME >= NOW() - INTERVAL 1 MINUTE;
    `;

    connection.query(query, (err, results) => {
        if (err) {
            return res.status(500).send('Database query error');
        }

        // 결과를 JSON 형태로 반환
        res.json(results[0]);
    });
});



// 서버 시작
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
