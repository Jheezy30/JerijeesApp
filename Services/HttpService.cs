using System;
using System.Net.Http;
using System.Text;
using System.Text.Json;
using System.Threading.Tasks;
using System.Windows;

namespace DemoApp.Services
{
    public class HttpService
    {
        private HttpClient client = new();
        public async Task<string> MakePredicton(string base64String, string endpointUrl = "http://127.0.0.1:8000/predict")
        {
            try
            {
                var payload = new
                {
                    sample = base64String
                };
                var jsonPayload = JsonSerializer.Serialize(payload);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                var response = await client.PostAsync(endpointUrl, content);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                return null;
            }
        }
        public async Task<string> Visualize(string base64String, string endpointUrl = "http://127.0.0.1:8000/viz")
        {
            try
            {
                var payload = new
                {
                    sample = base64String
                };
                var jsonPayload = JsonSerializer.Serialize(payload);
                var content = new StringContent(jsonPayload, Encoding.UTF8, "application/json");
                var response = await client.PostAsync(endpointUrl, content);
                response.EnsureSuccessStatusCode();
                return await response.Content.ReadAsStringAsync();
            }
            catch (Exception ex)
            {
                MessageBox.Show(ex.Message);
                return null;
            }
        }
    }
      
}
