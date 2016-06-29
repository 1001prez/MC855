
import java.io.IOException;
import java.io.File;
import java.util.StringTokenizer;
import java.io.FileInputStream;
import java.io.OutputStream;
import org.apache.commons.io.IOUtils.*;
import java.lang.reflect.Field;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.fs.FileSystem;
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.hdfs.DFSClient;
import org.apache.hadoop.hdfs.DistributedFileSystem;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;

public class Issue13264 {
	public static void main(String args[]) throws Exception
	{

		final Configuration conf = new Configuration();
		conf.addResource(new FileInputStream(new File("../etc/hadoop/core-site.xml")));
		conf.addResource(new FileInputStream(new File("../etc/hadoop/hdfs-site.xml")));

		final DistributedFileSystem newFileSystem = (DistributedFileSystem)FileSystem.get(conf);
		OutputStream outputStream = null;
		try
		{
			outputStream = newFileSystem.create(new Path("/user/hugo", "test1"));
			outputStream.write("test".getBytes());
		}
		catch (IOException e)
		{
			e.printStackTrace();
		}
		finally
		{
			try
			{
				if (outputStream != null)
					outputStream.close();//now this one will fail to close the stream
			}
			catch (IOException e)
			{
				e.printStackTrace();//this will list the thrown exception from DFSOutputStream->flushInternal->checkClosed
				//TODO the DFSOutputStream#close->dfsClient.endFileLease(fileId) is never getting closed
			}
		}

		Field field = DFSClient.class.getDeclaredField("filesBeingWritten");
		field.setAccessible(true);
		System.out.print("THIS SHOULD BE EMPTY: " + field.get(newFileSystem.getClient()));
	}
}
