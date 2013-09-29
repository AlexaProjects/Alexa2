/*  
Copyright (C) 2013 Alan Pipitone
    
Al'exa is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Al'exa is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Al'exa.  If not, see <http://www.gnu.org/licenses/>.
*/

using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Net;
using System.Net.Mail;
using System.Drawing;
using System.Drawing.Imaging;
using System.Drawing.Drawing2D;

namespace AlexaSendMail
{
    class Program
    {
        static void Main(string[] args)
        {
            try
            {
                /*
                int cnt = 0;
                foreach (string argument in args)
                {
                    Console.WriteLine(cnt.ToString() + "_" + argument);
                    cnt++;
                }*/

                string ErrorScreenFolder = args[0];
                string smtpHost = args[1];
                int smtpPort = Int32.Parse(args[2]);
                string mailFrom = args[3];
                string[] mailTo = args[4].Split(';');
                string subject = args[5];
                string mailMessage = args[6];
                string user = args[7];
                string password = args[8];
                string imgResizeFactor = args[9];
                string imgQuality = args[10];

                //init the smtp client
                SmtpClient client = new SmtpClient(smtpHost, smtpPort);

                VaryQualityLevel(ErrorScreenFolder, imgResizeFactor, imgQuality);

                //create the message object
                MailMessage message = new MailMessage();

                //set the "From" address
                message.From = new MailAddress(mailFrom, "Al'exa");

                foreach (string to in mailTo)
                {
                    message.To.Add(to);
                }

                message.Subject = subject;
                message.Body = mailMessage;

                //get all screenshots
                string[] array1 = Directory.GetFiles(ErrorScreenFolder, "*.jpg");

                foreach (string name in array1)
                {
                    Attachment attach = new Attachment(name);

                    message.Attachments.Add(attach);
                }

                if (user != "none" && password != "none")
                {
                    client.Credentials = new NetworkCredential(user, password);
                }

                client.Send(message);

                message.Dispose();
                //client.Dispose();

                foreach (string name in array1)
                {
                    File.Delete(name);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine(ex.Message);
                if (ex.InnerException != null) Console.WriteLine(ex.InnerException.Message);

            }

        }

        private static void VaryQualityLevel(string path, string resize, string imageQuality)
        {
            // Put all file names in root directory into array.
            string[] array1 = Directory.GetFiles(path);

            foreach (string name in array1)
            {
                try
                {
                    // Get a bitmap.
                    Bitmap bmp1 = new Bitmap(name);

                    float resizeFactor = float.Parse(resize);

                    resizeFactor = resizeFactor / 100;

                    if (resizeFactor != -1)
                    {
                        int newWidth = (int)(bmp1.Width * resizeFactor);
                        int newHeight = (int)(bmp1.Height * resizeFactor);

                        Image newImage = new Bitmap(newWidth, newHeight);
                        using (Graphics graphics = Graphics.FromImage(newImage))
                        {
                            graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                            graphics.DrawImage(bmp1, 0, 0, newWidth, newHeight);
                        }

                        bmp1 = (Bitmap)newImage;
                    }

                    ImageCodecInfo jgpEncoder = GetEncoder(ImageFormat.Jpeg);

                    // Create an Encoder object based on the GUID
                    // for the Quality parameter category.
                    System.Drawing.Imaging.Encoder myEncoder =
                        System.Drawing.Imaging.Encoder.Quality;

                    // Create an EncoderParameters object.
                    // An EncoderParameters object has an array of EncoderParameter
                    // objects. In this case, there is only one
                    // EncoderParameter object in the array.
                    EncoderParameters myEncoderParameters = new EncoderParameters(1);

                    EncoderParameter myEncoderParameter = new EncoderParameter(myEncoder,
                        Int64.Parse(imageQuality));

                    myEncoderParameters.Param[0] = myEncoderParameter;
                    bmp1.Save(name.Replace(".png", ".jpg"), jgpEncoder,
                        myEncoderParameters);

                    bmp1.Dispose();
                }
                catch
                {
                }
            }
        }

        private static ImageCodecInfo GetEncoder(ImageFormat format)
        {

            ImageCodecInfo[] codecs = ImageCodecInfo.GetImageDecoders();

            foreach (ImageCodecInfo codec in codecs)
            {
                if (codec.FormatID == format.Guid)
                {
                    return codec;
                }
            }
            return null;
        }
    }
}
