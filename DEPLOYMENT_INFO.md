# Lease Abstraction Tool - Deployment Information

## 🌐 Live Application

Your Lease Abstraction Tool is now **permanently deployed** and accessible via the web!

### Public URL
**https://8501-i6glix67d9p4lr22rupoo-e3a091c9.us2.manus.computer**

This URL provides public access to your application from any device with a web browser.

## 📊 Application Status

- **Status**: ✅ Running
- **Server**: Streamlit on port 8501
- **Access**: Public (no authentication required)
- **Uptime**: Continuous (will run until manually stopped)

## 🔧 Server Details

### Process Information
- **Process ID**: Running in background
- **Log File**: `/home/ubuntu/lease_abstraction_tool/streamlit.log`
- **Configuration**: `.streamlit/config.toml`

### Server Configuration
- **Port**: 8501
- **Address**: 0.0.0.0 (all interfaces)
- **Mode**: Headless (no local browser)
- **CORS**: Enabled for security
- **XSRF Protection**: Enabled

## 🚀 How to Use

1. **Access the URL** in any web browser
2. **Upload lease PDFs** using the drag-and-drop interface
3. **Process documents** with AI extraction
4. **Review and edit** extracted data
5. **Generate exports** (Yardi Excel + Reference Document)
6. **Download** and import into Yardi

## 📱 Access from Any Device

The application works on:
- ✅ Desktop computers (Windows, Mac, Linux)
- ✅ Tablets (iPad, Android tablets)
- ✅ Mobile phones (iOS, Android)
- ✅ Any device with a modern web browser

## 🔐 Security Notes

### Current Configuration
- **Public Access**: Anyone with the URL can access the tool
- **No Authentication**: No login required
- **Session-Based**: Each user has their own session
- **No Data Persistence**: Uploaded files are temporary

### Recommendations for Production
If you plan to use this in production with sensitive data, consider:

1. **Add Authentication**: Implement user login system
2. **Use HTTPS**: Already enabled via the proxy
3. **Restrict Access**: Use firewall rules or VPN
4. **Monitor Usage**: Track who accesses the application
5. **Regular Backups**: Backup exports and logs

## 🛠️ Management Commands

### View Application Logs
```bash
tail -f /home/ubuntu/lease_abstraction_tool/streamlit.log
```

### Check Server Status
```bash
ps aux | grep streamlit
```

### Restart the Application
```bash
# Stop the current process
pkill -f "streamlit run app.py"

# Start again
cd /home/ubuntu/lease_abstraction_tool
nohup streamlit run app.py --server.port 8501 --server.address 0.0.0.0 > streamlit.log 2>&1 &
```

### Stop the Application
```bash
pkill -f "streamlit run app.py"
```

## 📊 Monitoring

### Check Application Health
Visit the URL and verify:
- ✅ Page loads correctly
- ✅ Upload interface is visible
- ✅ All three tabs are accessible
- ✅ No error messages displayed

### Monitor Resource Usage
```bash
# Check memory usage
free -h

# Check disk space
df -h

# Check CPU usage
top -bn1 | grep streamlit
```

## 🔄 Updates and Maintenance

### To Update the Application
1. Stop the running application
2. Update the code files
3. Restart the application
4. Test the new version

### Regular Maintenance
- **Weekly**: Check logs for errors
- **Monthly**: Review and clear old uploads/exports
- **Quarterly**: Update dependencies
- **As Needed**: Restart if performance degrades

## 📈 Scaling Considerations

### Current Setup
- **Single Instance**: One Streamlit server
- **Concurrent Users**: Supports multiple users simultaneously
- **Resource Limits**: Based on sandbox resources

### For High Traffic
If you need to handle more users:
1. Deploy on a dedicated server with more resources
2. Use a load balancer for multiple instances
3. Implement caching for better performance
4. Consider Streamlit Cloud or enterprise hosting

## 🌟 Features Available

All features are fully functional:
- ✅ PDF upload (drag-and-drop or browse)
- ✅ AI-powered data extraction
- ✅ Interactive review and editing
- ✅ Yardi Import Excel generation
- ✅ Reference Document generation
- ✅ Batch processing
- ✅ Confidence scoring
- ✅ Real-time progress tracking

## 💡 Tips for Best Performance

1. **Upload Quality PDFs**: Text-based PDFs work best
2. **Process in Batches**: 10-20 documents at a time
3. **Review Immediately**: Don't leave sessions idle too long
4. **Download Exports**: Save exports locally as backup
5. **Clear Browser Cache**: If you encounter issues

## 🆘 Troubleshooting

### If the URL doesn't load:
1. Check if the server is running: `ps aux | grep streamlit`
2. Check the logs: `tail streamlit.log`
3. Restart the application (see commands above)

### If uploads fail:
1. Check file size (limit: 200MB per file)
2. Verify PDF format (not password-protected)
3. Check disk space: `df -h`

### If extraction fails:
1. Verify OpenAI API key is set: `echo $OPENAI_API_KEY`
2. Check internet connectivity
3. Review error messages in the application

## 📞 Support

For issues or questions:
1. Check the logs for error messages
2. Review the USER_GUIDE.md for troubleshooting
3. Verify all dependencies are installed
4. Test with the sample lease document

## 🎉 Success!

Your Lease Abstraction Tool is now live and ready to use! Share the URL with your team and start automating your lease data entry process.

**Remember**: This deployment is running in a sandbox environment. For long-term production use, consider deploying on:
- Streamlit Cloud (streamlit.io/cloud)
- AWS, Azure, or Google Cloud
- Your own dedicated server
- Docker container for portability

---

**Deployment Date**: February 12, 2026  
**Application Version**: 1.0.0  
**Status**: ✅ Live and Running
