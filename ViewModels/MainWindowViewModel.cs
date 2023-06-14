using DemoApp.Services;
using DemoApp.Utilities;
using Microsoft.Win32;
using Prism.Commands;
using Prism.Mvvm;
using Prism.Services.Dialogs;
using System;
using System.Windows.Controls;
using System.Windows;
using System.Windows.Media.Imaging;

namespace JerijeesApp.ViewModels
{
    public class MainWindowViewModel : BindableBase
    {
        private HttpService httpService = new HttpService();
        public string temp = "";
        private string selectedImage = "";
        public string SelectedImage
        {
            get { return selectedImage; }
            set { SetProperty(ref selectedImage, value); }
        }

        private BitmapImage results = new();
        public BitmapImage Results
        {
            get { return results; }
            set { SetProperty(ref results, value); }
        }

        private BitmapImage saliencyMap = new();
        public BitmapImage SaliencyMap
        {
            get { return saliencyMap; }
            set { SetProperty(ref saliencyMap, value); }
        }

        private string visible = "Collapsed";
        public string Visible
        {
            get { return visible; }
            set { SetProperty(ref visible, value); }
        }

        private bool canVisualize = false;
        public bool CanVisualize
        {
            get { return canVisualize; }
            set { SetProperty(ref canVisualize, value); }
        }

        private string pvisible = "Visible";
        public string PVisible
        {
            get { return pvisible; }
            set { SetProperty(ref pvisible, value); }
        }
        #region Commands
        public DelegateCommand LoadImagesCommand => new DelegateCommand(ExecuteLoadImagesCommand);
        public DelegateCommand SaliencyCommand => new DelegateCommand(ExecuteSaliencyCommand);
        private async void ExecuteLoadImagesCommand()
        {
            OpenFileDialog openFileDialog = new OpenFileDialog();
            openFileDialog.Filter = "Image files (*.jpg, *.jpeg, *.png) | *.jpg; *.jpeg; *.png";
            openFileDialog.RestoreDirectory = true;
            if (openFileDialog.ShowDialog() == true)
            {
                SelectedImage = openFileDialog.FileName;
                temp = openFileDialog.FileName;
            }
            var response = await httpService.MakePredicton(Converters.ImageToBase64Converter(this.SelectedImage));
            Results = Converters.Base64ToImage(response);
            PVisible = "Visible";
            Visible = "Collapsed";
            CanVisualize = true;
        }
        private async void ExecuteSaliencyCommand()
        {
            PVisible = "Collapsed";
            Visible = "Visible";
            var response = await httpService.Visualize(Converters.ImageToBase64Converter(this.temp));
            SaliencyMap = Converters.Base64ToImage(response);
        }
        #endregion
      
       


        public MainWindowViewModel()
        {

        }
       
    }
}
