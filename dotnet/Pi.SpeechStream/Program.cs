// See https://aka.ms/new-console-template for more information
using System.Diagnostics;


//ListAudioDevices();


Console.WriteLine("Recording....");
await using var stream = CaptureAudioStream(10);
await using var ws = File.OpenWrite("hello.wav");

Console.WriteLine("Saving...");
await stream.CopyToAsync(ws);
Console.WriteLine("Saved");

await using var stream2 = CaptureAudioStream(15);
await using var ws2 = File.OpenWrite("hello2.wav");

Console.WriteLine("Another 1...");
await stream2.CopyToAsync(ws2);


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


Stream CaptureAudioStream(int durationSeconds)
{
    var psi = new ProcessStartInfo
    {
        FileName = "arecord",
        Arguments = $"-D plughw:1,0 -d {durationSeconds} -f S16_LE -t wav -r 16000 -c 1 -",
        UseShellExecute = false,
        RedirectStandardOutput = true,
        CreateNoWindow = true
    };

    var process = new Process { StartInfo = psi };
    process.Start();
    return process.StandardOutput.BaseStream;
}
