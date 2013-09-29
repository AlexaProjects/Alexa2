namespace AlexaModule
{
    partial class Form1
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Form1));
            this.labelWizardIntro1 = new System.Windows.Forms.Label();
            this.pictureBox1 = new System.Windows.Forms.PictureBox();
            this.listBoxPythonVersion = new System.Windows.Forms.ListBox();
            this.buttonInsertManually = new System.Windows.Forms.Button();
            this.buttonOk = new System.Windows.Forms.Button();
            this.buttonCancel = new System.Windows.Forms.Button();
            this.textBoxInsertManually = new System.Windows.Forms.TextBox();
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).BeginInit();
            this.SuspendLayout();
            // 
            // labelWizardIntro1
            // 
            this.labelWizardIntro1.AutoSize = true;
            this.labelWizardIntro1.Location = new System.Drawing.Point(13, 253);
            this.labelWizardIntro1.Name = "labelWizardIntro1";
            this.labelWizardIntro1.Size = new System.Drawing.Size(464, 65);
            this.labelWizardIntro1.TabIndex = 0;
            this.labelWizardIntro1.Text = resources.GetString("labelWizardIntro1.Text");
            // 
            // pictureBox1
            // 
            this.pictureBox1.Image = ((System.Drawing.Image)(resources.GetObject("pictureBox1.Image")));
            this.pictureBox1.Location = new System.Drawing.Point(15, 5);
            this.pictureBox1.Name = "pictureBox1";
            this.pictureBox1.Size = new System.Drawing.Size(464, 236);
            this.pictureBox1.TabIndex = 1;
            this.pictureBox1.TabStop = false;
            // 
            // listBoxPythonVersion
            // 
            this.listBoxPythonVersion.FormattingEnabled = true;
            this.listBoxPythonVersion.Location = new System.Drawing.Point(17, 339);
            this.listBoxPythonVersion.Name = "listBoxPythonVersion";
            this.listBoxPythonVersion.Size = new System.Drawing.Size(462, 95);
            this.listBoxPythonVersion.TabIndex = 2;
            // 
            // buttonInsertManually
            // 
            this.buttonInsertManually.Location = new System.Drawing.Point(16, 457);
            this.buttonInsertManually.Name = "buttonInsertManually";
            this.buttonInsertManually.Size = new System.Drawing.Size(102, 23);
            this.buttonInsertManually.TabIndex = 3;
            this.buttonInsertManually.Text = "Insert Manually";
            this.buttonInsertManually.UseVisualStyleBackColor = true;
            this.buttonInsertManually.Click += new System.EventHandler(this.buttonInsertManually_Click);
            // 
            // buttonOk
            // 
            this.buttonOk.Location = new System.Drawing.Point(401, 457);
            this.buttonOk.Name = "buttonOk";
            this.buttonOk.Size = new System.Drawing.Size(75, 23);
            this.buttonOk.TabIndex = 4;
            this.buttonOk.Text = "Ok";
            this.buttonOk.UseVisualStyleBackColor = true;
            this.buttonOk.Click += new System.EventHandler(this.buttonOk_Click);
            // 
            // buttonCancel
            // 
            this.buttonCancel.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.buttonCancel.Location = new System.Drawing.Point(299, 457);
            this.buttonCancel.Name = "buttonCancel";
            this.buttonCancel.Size = new System.Drawing.Size(75, 23);
            this.buttonCancel.TabIndex = 5;
            this.buttonCancel.Text = "Cancel";
            this.buttonCancel.UseVisualStyleBackColor = true;
            this.buttonCancel.Click += new System.EventHandler(this.buttonCancel_Click);
            // 
            // textBoxInsertManually
            // 
            this.textBoxInsertManually.Location = new System.Drawing.Point(17, 339);
            this.textBoxInsertManually.Name = "textBoxInsertManually";
            this.textBoxInsertManually.Size = new System.Drawing.Size(462, 20);
            this.textBoxInsertManually.TabIndex = 6;
            this.textBoxInsertManually.Text = "Insert here the home path of Python";
            this.textBoxInsertManually.Visible = false;
            this.textBoxInsertManually.MouseClick += new System.Windows.Forms.MouseEventHandler(this.textBoxInsertManually_MouseClick);
            this.textBoxInsertManually.TextChanged += new System.EventHandler(this.textBoxInsertManually_TextChanged);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.Color.White;
            this.CancelButton = this.buttonCancel;
            this.ClientSize = new System.Drawing.Size(496, 492);
            this.Controls.Add(this.textBoxInsertManually);
            this.Controls.Add(this.buttonCancel);
            this.Controls.Add(this.buttonOk);
            this.Controls.Add(this.buttonInsertManually);
            this.Controls.Add(this.listBoxPythonVersion);
            this.Controls.Add(this.pictureBox1);
            this.Controls.Add(this.labelWizardIntro1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.MaximizeBox = false;
            this.MinimizeBox = false;
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Al\'exa 2.3.1 Python Module Setup";
            this.TopMost = true;
            this.Load += new System.EventHandler(this.Form1_Load);
            ((System.ComponentModel.ISupportInitialize)(this.pictureBox1)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelWizardIntro1;
        private System.Windows.Forms.PictureBox pictureBox1;
        private System.Windows.Forms.ListBox listBoxPythonVersion;
        private System.Windows.Forms.Button buttonInsertManually;
        private System.Windows.Forms.Button buttonOk;
        private System.Windows.Forms.Button buttonCancel;
        private System.Windows.Forms.TextBox textBoxInsertManually;
    }
}

