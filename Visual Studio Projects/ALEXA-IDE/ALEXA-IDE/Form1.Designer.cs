namespace ALEXA_IDE
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
            this.labelPython = new System.Windows.Forms.Label();
            this.listBoxPythonApp = new System.Windows.Forms.ListBox();
            this.buttonAccept = new System.Windows.Forms.Button();
            this.buttonCancel = new System.Windows.Forms.Button();
            this.buttonInsertManually = new System.Windows.Forms.Button();
            this.textBoxPythonApp = new System.Windows.Forms.TextBox();
            this.SuspendLayout();
            // 
            // labelPython
            // 
            this.labelPython.AutoSize = true;
            this.labelPython.Location = new System.Drawing.Point(13, 13);
            this.labelPython.Name = "labelPython";
            this.labelPython.Size = new System.Drawing.Size(286, 26);
            this.labelPython.TabIndex = 0;
            this.labelPython.Text = "Al\'exa has detected that this is the first time that you run the\r\nAL\'EXA-IDE, ple" +
                "ase choose the proper version of Python:";
            // 
            // listBoxPythonApp
            // 
            this.listBoxPythonApp.FormattingEnabled = true;
            this.listBoxPythonApp.Location = new System.Drawing.Point(16, 43);
            this.listBoxPythonApp.Name = "listBoxPythonApp";
            this.listBoxPythonApp.Size = new System.Drawing.Size(290, 82);
            this.listBoxPythonApp.TabIndex = 1;
            // 
            // buttonAccept
            // 
            this.buttonAccept.Location = new System.Drawing.Point(231, 131);
            this.buttonAccept.Name = "buttonAccept";
            this.buttonAccept.Size = new System.Drawing.Size(75, 23);
            this.buttonAccept.TabIndex = 2;
            this.buttonAccept.Text = "Accept";
            this.buttonAccept.UseVisualStyleBackColor = true;
            this.buttonAccept.Click += new System.EventHandler(this.buttonAccept_Click);
            // 
            // buttonCancel
            // 
            this.buttonCancel.Location = new System.Drawing.Point(150, 131);
            this.buttonCancel.Name = "buttonCancel";
            this.buttonCancel.Size = new System.Drawing.Size(75, 23);
            this.buttonCancel.TabIndex = 3;
            this.buttonCancel.Text = "Cancel";
            this.buttonCancel.UseVisualStyleBackColor = true;
            this.buttonCancel.Click += new System.EventHandler(this.buttonCancel_Click);
            // 
            // buttonInsertManually
            // 
            this.buttonInsertManually.Location = new System.Drawing.Point(16, 132);
            this.buttonInsertManually.Name = "buttonInsertManually";
            this.buttonInsertManually.Size = new System.Drawing.Size(97, 23);
            this.buttonInsertManually.TabIndex = 4;
            this.buttonInsertManually.Text = "Insert Manually";
            this.buttonInsertManually.UseVisualStyleBackColor = true;
            this.buttonInsertManually.Click += new System.EventHandler(this.buttonInsertManually_Click);
            // 
            // textBoxPythonApp
            // 
            this.textBoxPythonApp.Location = new System.Drawing.Point(16, 57);
            this.textBoxPythonApp.Name = "textBoxPythonApp";
            this.textBoxPythonApp.Size = new System.Drawing.Size(290, 20);
            this.textBoxPythonApp.TabIndex = 5;
            this.textBoxPythonApp.Text = "Insert here the full name of python executable";
            this.textBoxPythonApp.Visible = false;
            this.textBoxPythonApp.MouseClick += new System.Windows.Forms.MouseEventHandler(this.textBoxPythonApp_MouseClick);
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(324, 162);
            this.Controls.Add(this.textBoxPythonApp);
            this.Controls.Add(this.buttonInsertManually);
            this.Controls.Add(this.buttonCancel);
            this.Controls.Add(this.buttonAccept);
            this.Controls.Add(this.listBoxPythonApp);
            this.Controls.Add(this.labelPython);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Icon = ((System.Drawing.Icon)(resources.GetObject("$this.Icon")));
            this.Name = "Form1";
            this.StartPosition = System.Windows.Forms.FormStartPosition.CenterScreen;
            this.Text = "Choose Python Version";
            this.Load += new System.EventHandler(this.Form1_Load);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label labelPython;
        private System.Windows.Forms.ListBox listBoxPythonApp;
        private System.Windows.Forms.Button buttonAccept;
        private System.Windows.Forms.Button buttonCancel;
        private System.Windows.Forms.Button buttonInsertManually;
        private System.Windows.Forms.TextBox textBoxPythonApp;
    }
}

