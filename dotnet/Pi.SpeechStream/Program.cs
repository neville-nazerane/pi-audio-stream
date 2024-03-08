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
    var duration = TimeSpan.FromSeconds(10);

    // Create a MemoryStream to accumulate data.
    await using var outgoing = new MemoryStream();

    var stopwatch = Stopwatch.StartNew();
    byte[] buffer = new byte[4096]; // Buffer size can be adjusted based on expected data rates.
    int bytesRead;

    // Read and write to the outgoing MemoryStream until the time limit is reached.
    while ((bytesRead = await incoming.ReadAsync(buffer, 0, buffer.Length)) > 0 && stopwatch.Elapsed < duration)
    {
        Console.WriteLine(stopwatch.Elapsed);
        await outgoing.WriteAsync(buffer, 0, bytesRead);
    }

    // Rewind the outgoing MemoryStream to prepare for reading.
    outgoing.Seek(0, SeekOrigin.Begin);

    // Prepare the HttpRequestMessage with the content from the outgoing MemoryStream.
    using var request = new HttpRequestMessage(HttpMethod.Post, $"simplyRecord/{fileName}")
    {
        Content = new StreamContent(outgoing)
    };

    await Console.Out.WriteLineAsync("Sending Stream");
    await client.SendAsync(request);
    await Console.Out.WriteLineAsync("Request sent");
}


//async Task SendStreamToApiAsync(Stream incoming)
//{
//    string fileName = Guid.NewGuid().ToString("N");
//    await using var outgoing = new MemoryStream();
//    var request = new HttpRequestMessage(HttpMethod.Post, $"simplyRecord/{fileName}")
//    {
//        Content = new StreamContent(incoming)
//    };

//    var cancel = new CancellationTokenSource();
//    cancel.CancelAfter(TimeSpan.FromSeconds(20));

//    await Console.Out.WriteLineAsync("Sending Stream");
//    try
//    {
//        await client.SendAsync(request, cancel.Token);

//    }
//    catch (Exception ex)
//    {
//        Console.WriteLine("Exception thrown for request");
//        Console.WriteLine(ex);
//    }   
//    await Console.Out.WriteLineAsync("Request sent");

//    //await client.PostAsync($"completeFile/{fileName}", null);

//    //await Console.Out.WriteLineAsync("Completed");
//}

