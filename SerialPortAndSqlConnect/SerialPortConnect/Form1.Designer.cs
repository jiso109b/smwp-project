namespace SerialPortConnect
{
    partial class Form1
    {
        /// <summary>
        /// 필수 디자이너 변수입니다.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// 사용 중인 모든 리소스를 정리합니다.
        /// </summary>
        /// <param name="disposing">관리되는 리소스를 삭제해야 하면 true이고, 그렇지 않으면 false입니다.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form 디자이너에서 생성한 코드

        /// <summary>
        /// 디자이너 지원에 필요한 메서드입니다. 
        /// 이 메서드의 내용을 코드 편집기로 수정하지 마세요.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.label1 = new System.Windows.Forms.Label();
            this.saveFileDialog1 = new System.Windows.Forms.SaveFileDialog();
            this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
            this.cbbx_Port = new System.Windows.Forms.ComboBox();
            this.btn_Open = new System.Windows.Forms.Button();
            this.btn_Close = new System.Windows.Forms.Button();
            this.temp_label = new System.Windows.Forms.Label();
            this.received_TB = new System.Windows.Forms.TextBox();
            this.textBox_send = new System.Windows.Forms.TextBox();
            this.timer1 = new System.Windows.Forms.Timer(this.components);
            this.label3 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(193, 103);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(70, 15);
            this.label1.TabIndex = 0;
            this.label1.Text = "PortNumber";
            // 
            // cbbx_Port
            // 
            this.cbbx_Port.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.cbbx_Port.FormattingEnabled = true;
            this.cbbx_Port.Location = new System.Drawing.Point(171, 121);
            this.cbbx_Port.Name = "cbbx_Port";
            this.cbbx_Port.Size = new System.Drawing.Size(121, 23);
            this.cbbx_Port.TabIndex = 2;
            // 
            // btn_Open
            // 
            this.btn_Open.Location = new System.Drawing.Point(375, 97);
            this.btn_Open.Name = "btn_Open";
            this.btn_Open.Size = new System.Drawing.Size(119, 39);
            this.btn_Open.TabIndex = 8;
            this.btn_Open.Text = "Connect";
            this.btn_Open.UseVisualStyleBackColor = true;
            this.btn_Open.Click += new System.EventHandler(this.btn_Open_Click);
            // 
            // btn_Close
            // 
            this.btn_Close.Enabled = false;
            this.btn_Close.Location = new System.Drawing.Point(375, 142);
            this.btn_Close.Name = "btn_Close";
            this.btn_Close.Size = new System.Drawing.Size(119, 36);
            this.btn_Close.TabIndex = 9;
            this.btn_Close.Text = "Disconnect";
            this.btn_Close.UseVisualStyleBackColor = true;
            this.btn_Close.Click += new System.EventHandler(this.btn_Close_Click);
            // 
            // temp_label
            // 
            this.temp_label.Location = new System.Drawing.Point(168, 184);
            this.temp_label.Name = "temp_label";
            this.temp_label.Size = new System.Drawing.Size(74, 45);
            this.temp_label.TabIndex = 10;
            // 
            // received_TB
            // 
            this.received_TB.Location = new System.Drawing.Point(294, 181);
            this.received_TB.Multiline = true;
            this.received_TB.Name = "received_TB";
            this.received_TB.Size = new System.Drawing.Size(200, 80);
            this.received_TB.TabIndex = 11;
            // 
            // textBox_send
            // 
            this.textBox_send.Location = new System.Drawing.Point(142, 150);
            this.textBox_send.Name = "textBox_send";
            this.textBox_send.Size = new System.Drawing.Size(200, 25);
            this.textBox_send.TabIndex = 14;
            // 
            // timer1
            // 
            this.timer1.Interval = 1000;
            this.timer1.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(101, 184);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(40, 15);
            this.label3.TabIndex = 13;
            this.label3.Text = "PV : ";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(584, 361);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.textBox_send);
            this.Controls.Add(this.received_TB);
            this.Controls.Add(this.temp_label);
            this.Controls.Add(this.btn_Close);
            this.Controls.Add(this.btn_Open);
            this.Controls.Add(this.cbbx_Port);
            this.Controls.Add(this.label1);
            this.Name = "Form1";
            this.Text = "Form1";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.SaveFileDialog saveFileDialog1;
        private System.IO.Ports.SerialPort serialPort1;
        private System.Windows.Forms.ComboBox cbbx_Port;
        private System.Windows.Forms.Button btn_Open;
        private System.Windows.Forms.Button btn_Close;
        private System.Windows.Forms.Label temp_label;
        private System.Windows.Forms.TextBox received_TB;
        private System.Windows.Forms.TextBox textBox_send;
        private System.Windows.Forms.Timer timer1;
        private System.Windows.Forms.Label label3;
    }
}

