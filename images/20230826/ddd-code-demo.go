// ①用户接口层
// pkg: http_controller
func Routes(r *gin.Engine) {
    a := BuAlarmApi{}
    group := r.Group("/api/v1/bualarm")
    group.POST("/alarm", a.BuAlarm)
}
func (this *BuAlarmApi) BuAlarm(c *gin.Context) {
    bu := c.DefaultPostForm("bu", "")
    content := c.DefaultPostForm("content", "")
    username, err := this.GetUser(c)

    alarmDTO := dto.AlarmDTO{
        Budget_unit: bu,
        Content:     content,
        Sysname:     username,
    }
    err = BuAlarmApp.BuAlarm(alarmDTO)
    ...
    c.JSON(http.StatusOK, this.Success())
}

// ②应用层
// pkg: application
var BuAlarmApp = new(BuAlarmAppplication)
func (this *BuAlarmAppplication) BuAlarm(alarmDTO dto.AlarmDTO) error {
    alarmBO := bo.AlarmBO{
        Budget_unit: alarmDTO.Budget_unit,
        Title:       alarmDTO.Title,
        Content:     alarmDTO.Content,
    }
    // Go依赖注入
    domain := &domain.BuAlarm{BuChatRepo: repo.BuChatRepo, IMRepo: repoIm.IMRepo}
    err = domain.AlarmByBu(&alarmBO)
    ...
    return nil
}


// ③领域层
// pkg: domain
// SPI: IM基础设施接口定义 IMRepo
type IMRepo interface {
    SendIM(im *do.IM) error
}

// DomainService: 领域服务 AlarmByBu
type BuAlarm struct {
    IMRepo     dependency.IMRepo     // IM基础设施
}
func (this *BuAlarm) AlarmByBu(alarmBO *bo.AlarmBO) (err error) {
    bu := strings.TrimSpace(alarmBO.Budget_unit)
    buChatDO, err := this.BuChatRepo.GetBuChat(bu)
    ...
    imDO := do.IM{
        BU:      bu,
        Tos:     buChatDO.ChatIds,
        Content: alarmBO.Content,
    }
    err = this.IMRepo.SendIM(&imDO)
    ...
    return nil
}

// ④基础设施层
// pkg: infrastructure
var IMRepo = new(IMSender)
// SP: IMSender实现IMRepo规定的SPI
type IMSender struct {
}
func (this *IMSender) SendIM(im *do.IM) (err error) {
    SendChat(im.Tos, im.Content, createTitle(im.Content, im.Title))
    ...
    return nil
}
