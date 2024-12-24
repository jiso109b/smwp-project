using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using System.IO;
using System.IO.Ports;
using MySql.Data.MySqlClient;


namespace SerialPortConnect
{
    public partial class Form1 : Form
    {
        private float pv = 0;
        private bool isDisconnectedMessageShown = false; // 메시지 표시 여부 플래그
        public Form1()
        {
            InitializeComponent();

            GetAvailablePorts();

        }

        private void MySqlConnect(float pv)
        {
            try
            {
                string SERVER = "localhost";
                int PORT = 3306;
                string DATABASE = "tempDB"; 
                string ID = "root"; 
                string PW = "1234";
                string connStr = $"Server={SERVER};Port={PORT};Uid={ID};Pwd={PW};";

                // MySQL 연결 명령어
                MySqlConnection connection = new MySqlConnection(connStr);
                
                connection.Open();

                // 데이터베이스가 없으면 새로 생성, 있으면 아무 작업 안 함
                string checkDbQuery = $"CREATE DATABASE IF NOT EXISTS {DATABASE};";
                // MySqlCommand 클래스를 사용해 쿼리문을 MySQL로 전송
                MySqlCommand command = new MySqlCommand(checkDbQuery, connection);
                command.ExecuteNonQuery();

                // 데이터베이스 생성 후, 해당 데이터베이스로 연결
                connection.ChangeDatabase(DATABASE);


                // 테이블이 없으면 새로 생성, 있으면 아무 작업 안 함
                string createTableQuery = @"
                        CREATE TABLE IF NOT EXISTS tb (
                            TIME datetime not null primary key,
                            PV FLOAT NOT NULL
                        );";

                // MySqlCommand 클래스를 사용해 쿼리문을 MySQL로 전송
                command = new MySqlCommand(createTableQuery, connection);
                command.ExecuteNonQuery();

                string insertQuery = $"INSERT INTO {DATABASE}.tb VALUES (now(),{pv});";

                // MySqlCommand 클래스를 사용해 쿼리문을 MySQL로 전송
                command = new MySqlCommand(insertQuery, connection);
                // 데이터 삽입 실행 (INSERT 쿼리)
                command.ExecuteNonQuery();

                // SELECT 쿼리로 삽입된 데이터를 확인
                string selectQuery = $"SELECT * FROM tb;";  

                // SELECT 쿼리를 실행하여 삽입된 데이터 읽기
                command = new MySqlCommand(selectQuery, connection);


                // MySqlDataReader 클래스와 ExecuteReader() 함수를 이용해,받아온 정보를 reader에 저장
                MySqlDataReader reader = command.ExecuteReader();

                while (reader.Read())
                {
                    // 받아온 reader의 정보 중, name 열만 출력
                    Console.WriteLine($"TIME: {reader["TIME"]}, PV: {reader["PV"]}");
                }
                // MySQL 서버 연결 종료
                connection.Close();
            }
            catch (Exception ex)
            { Console.WriteLine(ex.Message.ToString()); }
        }
        

        private void GetAvailablePorts()
        {
            string[] ports = SerialPort.GetPortNames();
            cbbx_Port.Items.AddRange(ports);
            temp_label.Text = "00.0";
            textBox_send.Text = "010300010001D5CA";
        }


        private void btn_Open_Click(object sender, EventArgs e)
        {
            try
            {
                if (string.IsNullOrWhiteSpace(cbbx_Port.Text))
                {
                    MessageBox.Show("Please select a valid serial port.");
                    return;
                }

                
                serialPort1.PortName = cbbx_Port.Text;
                serialPort1.BaudRate = 9600;

                try
                {
                    serialPort1.Open();
                    MessageBox.Show("Connection Successful");
                }
                catch (UnauthorizedAccessException)
                {
                    MessageBox.Show("Access to the port is denied. Please check permissions or close other applications using the port.");
                    return;
                }
                catch (IOException)
                {
                    MessageBox.Show("The port could not be opened. It may not exist or is already in use.");
                    return;
                }
                catch (InvalidOperationException)
                {
                    MessageBox.Show("The port is already open.");
                    return;
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"An unexpected error occurred: {ex.Message}");
                    return;
                }

                btn_Open.Enabled = false;
                btn_Close.Enabled = true;
                serialPort1.DataReceived += new SerialDataReceivedEventHandler(serialPort1_DataReceived);
                timer1.Enabled = true;
               
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Unexpected error: {ex.Message}");
            }
        }

        private void serialPort1_DataReceived(object sender, SerialDataReceivedEventArgs e)  
        {
            this.Invoke(new EventHandler(SerialRecieve));  //메인 쓰레드와 수신 쓰레드의 충돌 방지를 위해 Invoke 사용. 
        }

        private StringBuilder receivedDataBuffer = new StringBuilder();

        private void SerialRecieve(object s, EventArgs e)
        {
            try
            {
                // 수신된 데이터의 바이트 수 확인
                int bytesToRead = serialPort1.BytesToRead;

                // 수신된 데이터를 읽어 버퍼에 저장
                byte[] buffers = new byte[bytesToRead];
                serialPort1.Read(buffers, 0, bytesToRead);

                // 버퍼에 저장된 데이터를 16진수 형식으로 변환하여 received_TB 출력
                foreach (byte buffer in buffers)
                {
                    // 데이터를 16진수 형식으로 변환하여 텍스트 박스에 추가
                    receivedDataBuffer.AppendFormat("{0:X2} ", buffer);

                }

                if (buffers.Length >= 5 && buffers[0] == 01 && buffers[1] == 03 && buffers[2] == 02)
                {
                    float calculatedValue = (buffers[3] * 256 + buffers[4]) / 10.0f;
                    // 계산된 값을 temp_label.Text에 문자열로 표시
                    temp_label.Text = calculatedValue.ToString();

                    pv = calculatedValue;

                    // MySQL에 삽입
                    MySqlConnect(pv);
                }

                // 데이터를 화면에 출력 (UI 스레드에서 안전하게 처리)
                received_TB.Invoke(new Action(() =>
                {
                    // 기존 텍스트를 덮어쓰지 않고 추가하는 방법
                    received_TB.AppendText(receivedDataBuffer.ToString() + "\r\n");
                    
                    // 자동 스크롤 설정
                    received_TB.SelectionStart = received_TB.Text.Length;
                    received_TB.ScrollToCaret();
                }));
            }
            catch (Exception ex)
            {
                // 예외 처리
                Console.WriteLine("Error: " + ex.Message);
            }
        }

        private void btn_Close_Click(object sender, EventArgs e)
        {
            serialPort1.Close();
            btn_Open.Enabled = true;
            btn_Close.Enabled = false;

        }

        private void timer1_Tick(object sender, EventArgs e)
        {
            try
            {
                if (serialPort1.IsOpen)
                {
                    byte[] byteArray = new byte[textBox_send.Text.Length / 2];

                    for (int i = 0; i < textBox_send.Text.Length; i += 2)
                    {
                        // 2글자씩 묶어서 하나의 바이트로 변환
                        string hexByte = textBox_send.Text.Substring(i, 2);
                        byteArray[i / 2] = Convert.ToByte(hexByte, 16);
                    }
                    serialPort1.Write(byteArray, 0, byteArray.Length);
                    isDisconnectedMessageShown = false;
                }
                else
                {
                    timer1.Enabled = false;
                    if (!isDisconnectedMessageShown)
                    {
                        MessageBox.Show("Serial port is not open. Please connect the device.");
                        isDisconnectedMessageShown = true;
                    }
                    
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show($"Error: {ex.Message}");
            }
        }
    }
}
