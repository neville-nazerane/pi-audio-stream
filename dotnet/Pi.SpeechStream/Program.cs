// See https://aka.ms/new-console-template for more information
using System.Diagnostics;



var client = new HttpClient
{
    BaseAddress = new(args[0])
};


await using var stream = CaptureAudioStream();

await SendStreamToApiAsync(stream);

//ListAudioDevices();



static void ListAudioDevices()
{
    ProcessStartInfo psi = new ProcessStartInfo
    {
        FileName = "arecord",
        Arguments = "-l", // Lists the recording sound devices
        UseShellExecute = false,
        RedirectStandardOutput = true,
        CreateNoWindow = true
    };

    try
    {
        using (Process process = Process.Start(psi))
        {
            using (System.IO.StreamReader reader = process.StandardOutput)
            {
                string result = reader.ReadToEnd();
                Console.Write(result);
            }
        }
    }
    catch (Exception ex)
    {
        Console.WriteLine($"An error occurred: {ex.Message}");
    }
}


Stream CaptureAudioStream()
{
    var psi = new ProcessStartInfo
    {
        FileName = "arecord",
        Arguments = $"-D plughw:1,0 -f S16_LE -t wav -r 16000 -c 1 -",
        UseShellExecute = false,
        RedirectStandardOutput = true,
        CreateNoWindow = true
    };

    var process = new Process { StartInfo = psi };
    process.Start();
    return process.StandardOutput.BaseStream;
}



async Task SendStreamToApiAsync(Stream incoming)
{
    string fileName = Guid.NewGuid().ToString("N");
    await using var outgoing = new MemoryStream();
    var request = new HttpRequestMessage(HttpMethod.Post, $"audioToSpecificFile/{fileName}")
    {
        Content = new StreamContent(incoming)
    };

    var cancel = new CancellationTokenSource();
    cancel.CancelAfter(TimeSpan.FromSeconds(20));

    await Console.Out.WriteLineAsync("Sending Stream");
    try
    {
        await client.SendAsync(request, cancel.Token);

    }
    catch (Exception ex)
    {
        Console.WriteLine("Exception thrown for request");
        Console.WriteLine(ex);
    }   
    await Console.Out.WriteLineAsync("Request sent");

    await client.PostAsync($"completeFile/{fileName}", null);

    await Console.Out.WriteLineAsync("Completed");
}